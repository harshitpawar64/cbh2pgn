import struct
from collections.abc import Iterator
from pathlib import Path

from cbh2pgn.models import Player

_RECORD_STRUCT = struct.Struct(">9x 30s 20s 8x")


class CBPReader:
    HEADER_SIZE = 32
    RECORD_SIZE = 67

    def __init__(self, file_path: str | Path) -> None:
        self.file_path = Path(file_path)
        self._data = memoryview(self._load())

    def __len__(self) -> int:
        return self.total_players

    def __iter__(self) -> Iterator[Player]:
        return (self[i] for i in range(len(self)))

    def __getitem__(self, index: int) -> Player:
        if index < 0:
            index += len(self)

        if not 0 <= index < len(self):
            raise IndexError(f"Player index {index} out of range (0..{len(self) - 1})")

        offset = self.HEADER_SIZE + (index * self.RECORD_SIZE)
        last_raw, first_raw = _RECORD_STRUCT.unpack_from(self._data, offset)

        last_name = self._decode_string(last_raw)
        first_name = self._decode_string(first_raw)

        return Player(id=index, last_name=last_name, first_name=first_name)

    @property
    def total_players(self) -> int:
        return max(0, (len(self._data) - self.HEADER_SIZE) // self.RECORD_SIZE)

    def _load(self) -> bytes:
        try:
            return self.file_path.read_bytes()
        except OSError as e:
            raise RuntimeError(f"Failed to read CBP file at {self.file_path}") from e

    @staticmethod
    def _decode_string(raw_bytes: bytes) -> str:
        return (
            raw_bytes.partition(b"\x00")[0].decode("cp1252", errors="replace").strip()
        )
