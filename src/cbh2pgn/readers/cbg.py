from pathlib import Path

from cbh2pgn.models import DecodedGame
from cbh2pgn.readers._cbg_utils import (
    ABS_TO_XY,
    CASTLING_ROOKS,
    DEOBFUSCATE_2B,
    FILES,
    MASK_GAME_LENGTH,
    MASK_IS_960,
    MASK_IS_ENCODED,
    MASK_SPECIAL_ENCODING,
    MASK_START_WITH_INITIAL,
    OPCODE_TABLE,
    PROMOTION_MAP,
    RANKS,
    SAN_PIECE_CHARS,
    SAN_PROMOTION_CHARS,
    SPECIAL_CODES,
    BoardGrid,
    Piece,
    PieceLocations,
    create_initial_board,
    decode_custom_position,
    get_disambiguation,
    handle_capture,
    update_castled_rook,
)


class CBGReader:
    def __init__(self, file_path: str | Path) -> None:
        self.file_path = Path(file_path)
        self._data = memoryview(self._load())

    def decode_game(self, moves_offset: int) -> DecodedGame:
        if moves_offset <= 0 or moves_offset + 4 > len(self._data):
            return DecodedGame(error="Invalid moves offset")

        size_info = int.from_bytes(self._data[moves_offset : moves_offset + 4], "big")
        not_initial = (size_info & MASK_START_WITH_INITIAL) >> 30
        not_encoded = (size_info & MASK_IS_ENCODED) >> 31
        is_960 = bool(size_info & MASK_IS_960)
        special_encoding = (size_info & MASK_SPECIAL_ENCODING) >> 26
        game_length = size_info & MASK_GAME_LENGTH

        if (
            not_encoded
            or is_960
            or special_encoding
            or moves_offset + game_length > len(self._data)
        ):
            return DecodedGame(error="Unsupported game format or encoding flag.")

        try:
            if not_initial:
                (board_grid, piece_locations, fen, is_white_turn, start_move_number) = (
                    decode_custom_position(self._data, moves_offset)
                )
                moves_bytes = self._data[moves_offset + 32 : moves_offset + game_length]
                san_str = _decode_san_bytes(
                    moves_bytes,
                    board_grid,
                    piece_locations,
                    is_white_turn=is_white_turn,
                    start_move_number=start_move_number,
                )
                return DecodedGame(moves=san_str, fen=fen)

            board_grid, piece_locations = create_initial_board()
            moves_bytes = self._data[moves_offset + 4 : moves_offset + game_length]
            san_str = _decode_san_bytes(moves_bytes, board_grid, piece_locations)
            return DecodedGame(moves=san_str)
        except (IndexError, KeyError, ValueError, RuntimeError) as e:
            return DecodedGame(error=f"Failed to decode moves: {e}")

    def _load(self) -> bytes:
        try:
            return self.file_path.read_bytes()
        except OSError as e:
            raise RuntimeError(f"Failed to read CBG file at {self.file_path}") from e


def _move(
    piece_locations: PieceLocations,
    board_grid: BoardGrid,
    piece_type: Piece | int,
    piece_index: int,
    from_file: int,
    from_rank: int,
    to_file: int,
    to_rank: int,
    is_capture: bool,
    token: int,
) -> None:
    board_grid[from_file][from_rank] = (Piece.NONE, None)
    if is_capture:
        target_type, target_piece_index = board_grid[to_file][to_rank]
        handle_capture(
            piece_locations,
            board_grid,
            piece_type,
            from_file,
            from_rank,
            to_file,
            target_type,
            target_piece_index,
        )

    board_grid[to_file][to_rank] = (piece_type, piece_index)
    piece_locations[piece_type][piece_index] = (to_file, to_rank)

    if token == 0x76 or token == 0xB5:
        castling_info = CASTLING_ROOKS.get((piece_type, token))
        if castling_info is not None:
            rook_type, rook_src_file, rook_dst_file, rook_rank = castling_info
            update_castled_rook(
                piece_locations,
                board_grid,
                rook_type,
                rook_src_file,
                rook_dst_file,
                rook_rank,
            )


def _move_2b(
    piece_locations: PieceLocations,
    board_grid: BoardGrid,
    moving_piece_type: Piece | int,
    moving_piece_index: int,
    from_file: int,
    from_rank: int,
    to_file: int,
    to_rank: int,
    is_capture: bool,
    promotion_code: int,
) -> None:
    board_grid[from_file][from_rank] = (Piece.NONE, None)
    if is_capture:
        target_type, target_piece_index = board_grid[to_file][to_rank]
        handle_capture(
            piece_locations,
            board_grid,
            moving_piece_type,
            from_file,
            from_rank,
            to_file,
            target_type,
            target_piece_index,
        )

    if (
        moving_piece_type in (Piece.W_KING, Piece.B_KING)
        and abs(to_file - from_file) == 2
    ):
        rook_type = Piece.W_ROOK if moving_piece_type == Piece.W_KING else Piece.B_ROOK
        src_file, dst_file = (7, 5) if to_file == 6 else (0, 3)
        update_castled_rook(
            piece_locations, board_grid, rook_type, src_file, dst_file, from_rank
        )

    if moving_piece_type not in (Piece.W_PAWN, Piece.B_PAWN):
        board_grid[to_file][to_rank] = (moving_piece_type, moving_piece_index)
        piece_locations[moving_piece_type][moving_piece_index] = (to_file, to_rank)
    else:
        if promotion_options := PROMOTION_MAP.get((moving_piece_type, to_rank)):
            piece_locations[moving_piece_type][moving_piece_index] = None
            selected_index = promotion_code & 3
            promotion_piece_type = promotion_options[selected_index]
            try:
                free_slot = piece_locations[promotion_piece_type].index(None)
            except ValueError:
                piece_locations[promotion_piece_type].append(None)
                free_slot = len(piece_locations[promotion_piece_type]) - 1
            piece_locations[promotion_piece_type][free_slot] = (to_file, to_rank)
            board_grid[to_file][to_rank] = (promotion_piece_type, free_slot)
        else:
            board_grid[to_file][to_rank] = (moving_piece_type, moving_piece_index)
            piece_locations[moving_piece_type][moving_piece_index] = (to_file, to_rank)


def _decode_san_bytes(
    game_bytes: memoryview | bytes,
    board_grid: BoardGrid,
    piece_locations: PieceLocations,
    is_white_turn: bool = True,
    start_move_number: int = 1,
) -> str:
    processed_moves = 0
    san_tokens: list[str] = []
    byte_offset = 0
    total_bytes = len(game_bytes)
    move_number = start_move_number

    while byte_offset < total_bytes:
        token = (game_bytes[byte_offset] - processed_moves) % 256
        if token not in SPECIAL_CODES:
            processed_moves = (processed_moves + 1) % 256
        if token == 0x9F:
            byte_offset += 1
            continue
        if token == 0xAA:
            if is_white_turn:
                san_tokens.append(f"{move_number}. --")
            else:
                if not san_tokens:
                    san_tokens.append(f"{move_number}... --")
                else:
                    san_tokens.append("--")
                move_number += 1
            is_white_turn = not is_white_turn
            byte_offset += 1
            continue
        if token == 0x29:
            if byte_offset + 2 >= total_bytes:
                break
            byte1 = DEOBFUSCATE_2B[
                (game_bytes[byte_offset + 1] - processed_moves) % 256
            ]
            byte2 = DEOBFUSCATE_2B[
                (game_bytes[byte_offset + 2] - processed_moves) % 256
            ]
            raw_move = (byte1 << 8) | byte2
            from_file, from_rank = ABS_TO_XY[raw_move & 0x3F]
            to_file, to_rank = ABS_TO_XY[(raw_move >> 6) & 0x3F]
            promotion_code = (raw_move >> 12) & 0x3

            moving_piece_type, moving_piece_index = board_grid[from_file][from_rank]
            is_pawn = moving_piece_type in (Piece.W_PAWN, Piece.B_PAWN)
            is_king = moving_piece_type in (Piece.W_KING, Piece.B_KING)
            target_type, _ = board_grid[to_file][to_rank]
            is_capture = target_type != Piece.NONE or (is_pawn and from_file != to_file)

            if is_king and abs(to_file - from_file) == 2:
                san_move = "O-O" if to_file == 6 else "O-O-O"
            elif is_pawn:
                dest = f"{FILES[to_file]}{RANKS[to_rank]}"
                promotion_suffix = ""
                if PROMOTION_MAP.get((moving_piece_type, to_rank)):
                    promotion_suffix = f"={SAN_PROMOTION_CHARS[promotion_code & 3]}"
                san_move = (
                    f"{FILES[from_file]}x{dest}{promotion_suffix}"
                    if is_capture
                    else f"{dest}{promotion_suffix}"
                )
            else:
                piece_char = SAN_PIECE_CHARS[moving_piece_type]
                disambiguation = (
                    get_disambiguation(
                        board_grid,
                        piece_locations,
                        moving_piece_type,
                        moving_piece_index,
                        from_file,
                        from_rank,
                        to_file,
                        to_rank,
                    )
                    if moving_piece_type not in (Piece.W_KING, Piece.B_KING)
                    else ""
                )
                capture_char = "x" if is_capture else ""
                dest = f"{FILES[to_file]}{RANKS[to_rank]}"
                san_move = f"{piece_char}{disambiguation}{capture_char}{dest}"

            _move_2b(
                piece_locations,
                board_grid,
                moving_piece_type,
                moving_piece_index,
                from_file,
                from_rank,
                to_file,
                to_rank,
                is_capture,
                promotion_code,
            )
            if is_white_turn:
                san_tokens.append(f"{move_number}. {san_move}")
            else:
                if not san_tokens:
                    san_tokens.append(f"{move_number}... {san_move}")
                else:
                    san_tokens.append(san_move)
                move_number += 1
            is_white_turn = not is_white_turn
            processed_moves = (processed_moves + 1) % 256
            byte_offset += 3
            continue
        if token == 0xDC:
            break
        if opcode_info := OPCODE_TABLE[token]:
            white_type, black_type, piece_index, dx, dy, is_pawn = opcode_info
            piece_type = white_type if is_white_turn else black_type
            pawn_flip = not is_white_turn and is_pawn
            actual_dx, actual_dy = (-dx, -dy) if pawn_flip else (dx, dy)

            coords = piece_locations[piece_type][piece_index]
            if coords is not None:
                from_file, from_rank = coords
                to_file, to_rank = (
                    (from_file + actual_dx) % 8,
                    (from_rank + actual_dy) % 8,
                )
                target_type, _ = board_grid[to_file][to_rank]
                is_capture = target_type != Piece.NONE or (is_pawn and actual_dx != 0)

                if token == 0x76:
                    san_move = "O-O"
                elif token == 0xB5:
                    san_move = "O-O-O"
                elif is_pawn:
                    dest = f"{FILES[to_file]}{RANKS[to_rank]}"
                    san_move = f"{FILES[from_file]}x{dest}" if is_capture else dest
                else:
                    piece_char = SAN_PIECE_CHARS[piece_type]
                    disambiguation = ""
                    if piece_type not in (Piece.W_KING, Piece.B_KING):
                        disambiguation = get_disambiguation(
                            board_grid,
                            piece_locations,
                            piece_type,
                            piece_index,
                            from_file,
                            from_rank,
                            to_file,
                            to_rank,
                        )
                    capture_char = "x" if is_capture else ""
                    dest = f"{FILES[to_file]}{RANKS[to_rank]}"
                    san_move = f"{piece_char}{disambiguation}{capture_char}{dest}"

                _move(
                    piece_locations,
                    board_grid,
                    piece_type,
                    piece_index,
                    from_file,
                    from_rank,
                    to_file,
                    to_rank,
                    is_capture,
                    token,
                )
                if is_white_turn:
                    san_tokens.append(f"{move_number}. {san_move}")
                else:
                    if not san_tokens:
                        san_tokens.append(f"{move_number}... {san_move}")
                    else:
                        san_tokens.append(san_move)
                    move_number += 1
                is_white_turn = not is_white_turn
        byte_offset += 1
    return " ".join(san_tokens)
