import typer

from sni.database import session_scope
from sni.search.rebuild import rebuild_search_index

app = typer.Typer(help="Manage the search index.")


@app.command()
def rebuild():
    """Rebuild the denormalized search_index (DELETE + bulk INSERT, one txn)."""
    typer.echo("Rebuilding search index...")
    with session_scope() as session:
        rebuild_search_index(session)
    typer.echo("Finished rebuilding search index!")


if __name__ == "__main__":
    app()
