from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Player:
    id: int
    last_name: str
    first_name: str

    @property
    def full_name(self) -> str:
        if self.last_name and self.first_name:
            return f"{self.last_name}, {self.first_name}"
        return self.last_name or self.first_name or "?"


@dataclass(frozen=True, slots=True)
class Tournament:
    id: int
    event: str
    site: str


@dataclass(frozen=True, slots=True)
class CBHRecord:
    game_id: int
    moves_offset: int
    white_player_id: int
    black_player_id: int
    tournament_id: int
    year: int
    month: int
    day: int
    result: str
    round: int
    sub_round: int
    white_elo: int
    black_elo: int
    eco: str
    is_deleted: bool

    @property
    def date_str(self) -> str:
        y_str = f"{self.year:04d}" if self.year > 0 else "????"
        m_str = f"{self.month:02d}" if self.month > 0 else "??"
        d_str = f"{self.day:02d}" if self.day > 0 else "??"
        return f"{y_str}.{m_str}.{d_str}"

    @property
    def round_str(self) -> str:
        if self.round > 0 and self.sub_round > 0:
            return f"{self.round}.{self.sub_round}"
        elif self.round > 0:
            return str(self.round)
        else:
            return "?"


@dataclass(frozen=True, slots=True)
class GameMetadata:
    game_id: int
    event: str
    site: str
    date: str
    round: str
    white: str
    black: str
    result: str
    white_elo: int
    black_elo: int
    eco: str
    moves_offset: int
    is_deleted: bool
