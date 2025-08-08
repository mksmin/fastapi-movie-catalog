import typer

from typing import Annotated
from rich import print

app = typer.Typer(
    rich_markup_mode="rich",
    no_args_is_help=True,
)


@app.command(
    help="Greet user by [bold]name[/bold].",
)
def hello(
    name: Annotated[str, typer.Argument(help="Name of the user.")],
):
    print(f"[bold]Hello [green]{name}[/green]![/bold]")
