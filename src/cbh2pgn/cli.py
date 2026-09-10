from pathlib import Path
from typing import Annotated

import typer

from cbh2pgn import __version__
from cbh2pgn.database import CBHDatabase

app = typer.Typer(no_args_is_help=True)


def _report_errors(errors: list[tuple[int, str]]) -> None:
    if not errors:
        return

    count = len(errors)
    typer.secho(
        f"\nWarning: {count} game{'s' if count != 1 else ''} could not be decoded:",
        err=True,
    )
    max_display = 10
    for game_id, error_message in errors[:max_display]:
        typer.echo(f"  - Game {game_id}: {error_message}", err=True)
    if count > max_display:
        typer.secho(f"  ... and {count - max_display} more.", err=True)


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
    errors: list[tuple[int, str]] = []

    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        with open(output, "w", encoding="utf-8") as output_file:
            for game in db:
                if not include_deleted and game.is_deleted:
                    continue
                if game.error:
                    errors.append((game.game_id, game.error))
                output_file.write(f"{game.to_pgn()}\n")
    else:
        for game in db:
            if not include_deleted and game.is_deleted:
                continue
            if game.error:
                errors.append((game.game_id, game.error))
            print(f"{game.to_pgn()}\n", end="")

    _report_errors(errors)


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
