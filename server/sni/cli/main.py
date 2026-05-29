import typer

from .commands import cdn, content, search

app = typer.Typer()
app.add_typer(content.app, name="content")
app.add_typer(cdn.app, name="cdn")
app.add_typer(search.app, name="search")


if __name__ == "__main__":
    app()
