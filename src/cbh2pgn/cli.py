from typing import Annotated

import typer

from cbh2pgn import __version__

app = typer.Typer()


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
