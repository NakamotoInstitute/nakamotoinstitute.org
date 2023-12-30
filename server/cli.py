import typer
from typing_extensions import Annotated

from sni.content.update import update_content

app = typer.Typer(help="Manage content.")


@app.command()
def initialize(force: Annotated[bool, typer.Option(help="Say hi formally.")] = False):
    """
    Initialize and seed database.
    """
    typer.echo("Initializing database...")
    update_content(force)
    typer.echo("Finished importing data!")


if __name__ == "__main__":
    app()
