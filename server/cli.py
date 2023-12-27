import typer

from sni.content.update import update_content

app = typer.Typer(help="Manage content.")


@app.command()
def initialize():
    """
    Initialize and seed database.
    """
    typer.echo("Initializing database...")
    update_content()
    typer.echo("Finished importing data!")


if __name__ == "__main__":
    app()
