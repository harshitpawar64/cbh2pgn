import struct
from collections.abc import Iterator
from pathlib import Path

from cbh2pgn.models import Tournament

_RECORD_STRUCT = struct.Struct(">9x 40s 30s 20x")


class CBTReader:
    HEADER_SIZE = 32
    RECORD_SIZE = 99

    def __init__(self, file_path: str | Path) -> None:
        self.file_path = Path(file_path)
        self._data = memoryview(self._load())

    def __len__(self) -> int:
        return self.total_tournaments

    def __iter__(self) -> Iterator[Tournament]:
        return (self[i] for i in range(len(self)))

    def __getitem__(self, index: int) -> Tournament:
        if index < 0:
            index += len(self)

        if not 0 <= index < len(self):
            raise IndexError(
                f"Tournament index {index} out of range (0..{len(self) - 1})"
            )

        offset = self.HEADER_SIZE + (index * self.RECORD_SIZE)
        event_raw, site_raw = _RECORD_STRUCT.unpack_from(self._data, offset)

        event = self._decode_string(event_raw)
        site = self._decode_string(site_raw)

        return Tournament(id=index, event=event, site=site)

    @property
    def total_tournaments(self) -> int:
        return max(0, (len(self._data) - self.HEADER_SIZE) // self.RECORD_SIZE)

    def _load(self) -> bytes:
        try:
            return self.file_path.read_bytes()
        except OSError as e:
            raise RuntimeError(f"Failed to read CBT file at {self.file_path}") from e

    @staticmethod
    def _decode_string(raw_bytes: bytes) -> str:
        return (
            raw_bytes.partition(b"\x00")[0].decode("cp1252", errors="replace").strip()
        )
