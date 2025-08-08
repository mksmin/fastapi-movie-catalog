__all__ = ("app",)

import typer

from .hello import app as hello_app

app = typer.Typer(
    no_args_is_help=True,
    rich_markup_mode="rich",
)


@app.callback()
def callback():
    """
    some text
    """


app.add_typer(hello_app)
