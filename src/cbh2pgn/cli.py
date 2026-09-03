from pathlib import Path
from typing import Annotated

import typer

from cbh2pgn import __version__
from cbh2pgn.database import CBHDatabase

app = typer.Typer(no_args_is_help=True)


@app.command()
def convert(
    database: Annotated[
        Path, typer.Argument(help="Path to the ChessBase database (.cbh file).")
    ],
    output: Annotated[
        Path | None,
        typer.Option(
            "-o", "--output", help="Output PGN file path. Defaults to stdout."
        ),
    ] = None,
    include_deleted: Annotated[
        bool, typer.Option("--include-deleted", help="Include deleted games in output.")
    ] = False,
) -> None:
    """Convert a ChessBase database to PGN format."""

    db = CBHDatabase(database)

    games = (
        f"{game.to_pgn()}\n" for game in db if include_deleted or not game.is_deleted
    )

    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        with open(output, "w", encoding="utf-8") as f:
            f.writelines(games)
    else:
        for game in games:
            print(game, end="")


def version_callback(value: bool) -> None:
    if value:
        print(f"cbh2pgn {__version__}")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            "-V",
            callback=version_callback,
            is_eager=True,
            help="Show version and exit.",
        ),
    ] = False,
) -> None: ...
