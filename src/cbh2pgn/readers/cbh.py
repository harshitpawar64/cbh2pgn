import struct
from collections.abc import Iterator
from pathlib import Path

from cbh2pgn.models import CBHRecord

_ECO_LETTERS = ("A", "B", "C", "D", "E")
_RESULTS = {0: "0-1", 1: "1/2-1/2", 2: "1-0"}
_RECORD_STRUCT = struct.Struct(">B I 4x 3s 3s 3s 6x 3s B 1x B B H H H 9x")


class CBHReader:
    HEADER_SIZE = 46
    RECORD_SIZE = 46

    def __init__(self, file_path: str | Path) -> None:
        self.file_path = Path(file_path)
        self._data = memoryview(self._load())

    def __len__(self) -> int:
        return self.total_games

    def __iter__(self) -> Iterator[CBHRecord]:
        return (self[i] for i in range(len(self)))

    def __getitem__(self, index: int) -> CBHRecord:
        if index < 0:
            index += len(self)

        if not 0 <= index < len(self):
            raise IndexError(f"Game index {index} out of range (0..{len(self) - 1})")

        offset = self.HEADER_SIZE + (index * self.RECORD_SIZE)
        (
            flags,
            moves_offset,
            white_id,
            black_id,
            tournament_id,
            date_raw,
            result_code,
            round_num,
            sub_round,
            white_elo,
            black_elo,
            eco_raw,
        ) = _RECORD_STRUCT.unpack_from(self._data, offset)

        year, month, day = self._decode_date(int.from_bytes(date_raw))

        return CBHRecord(
            game_id=index,
            moves_offset=moves_offset,
            white_player_id=int.from_bytes(white_id),
            black_player_id=int.from_bytes(black_id),
            tournament_id=int.from_bytes(tournament_id),
            year=year,
            month=month,
            day=day,
            result=_RESULTS.get(result_code, "*"),
            round=round_num,
            sub_round=sub_round,
            white_elo=white_elo,
            black_elo=black_elo,
            eco=self._decode_eco(eco_raw),
            is_deleted=(flags >= 128),
        )

    @property
    def total_games(self) -> int:
        return max(0, (len(self._data) - self.HEADER_SIZE) // self.RECORD_SIZE)

    def _load(self) -> bytes:
        try:
            return self.file_path.read_bytes()
        except OSError as e:
            raise RuntimeError(f"Failed to read CBH file at {self.file_path}") from e

    @staticmethod
    def _decode_date(date: int) -> tuple[int, int, int]:
        day = date & 0x1F
        month = (date >> 5) & 0x0F
        year = date >> 9
        return year, month, day

    @staticmethod
    def _decode_eco(eco_index: int) -> str:
        eco_index >>= 7

        if not (1 <= eco_index <= 500):
            return ""

        letter_index, number = divmod(eco_index - 1, 100)
        return f"{_ECO_LETTERS[letter_index]}{number:02d}"
