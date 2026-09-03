from collections.abc import Iterator
from pathlib import Path
from typing import overload

from cbh2pgn.models import GameMetadata
from cbh2pgn.readers.cbh import CBHReader
from cbh2pgn.readers.cbp import CBPReader
from cbh2pgn.readers.cbt import CBTReader


class CBHDatabase:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

        self.cbh = CBHReader(self.path.with_suffix(".cbh"))

        cbp_path = self.path.with_suffix(".cbp")
        self.cbp = CBPReader(cbp_path) if cbp_path.exists() else None

        cbt_path = self.path.with_suffix(".cbt")
        self.cbt = CBTReader(cbt_path) if cbt_path.exists() else None

    def __len__(self) -> int:
        return len(self.cbh)

    def __iter__(self) -> Iterator[GameMetadata]:
        return (self[i] for i in range(len(self)))

    @overload
    def __getitem__(self, index: int) -> GameMetadata: ...

    @overload
    def __getitem__(self, index: slice) -> list[GameMetadata]: ...

    def __getitem__(self, index: int | slice) -> GameMetadata | list[GameMetadata]:
        if isinstance(index, slice):
            return [self[i] for i in range(*index.indices(len(self)))]

        if index < 0:
            index += len(self)

        if not (0 <= index < len(self)):
            raise IndexError(f"Game index {index} out of range (0..{len(self) - 1})")

        record = self.cbh[index]

        white = "?"
        if self.cbp and 0 <= record.white_player_id < len(self.cbp):
            white = self.cbp[record.white_player_id].full_name

        black = "?"
        if self.cbp and 0 <= record.black_player_id < len(self.cbp):
            black = self.cbp[record.black_player_id].full_name

        event = "?"
        site = "?"
        if self.cbt and 0 <= record.tournament_id < len(self.cbt):
            tournament = self.cbt[record.tournament_id]
            event = tournament.event or "?"
            site = tournament.site or "?"

        return GameMetadata(
            game_id=record.game_id,
            event=event,
            site=site,
            date=record.date_str,
            round=record.round_str,
            white=white,
            black=black,
            result=record.result,
            white_elo=record.white_elo,
            black_elo=record.black_elo,
            eco=record.eco,
            moves_offset=record.moves_offset,
            is_deleted=record.is_deleted,
        )
