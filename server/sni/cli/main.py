import typer

from .commands import cdn, content

app = typer.Typer()
app.add_typer(content.app, name="content")
app.add_typer(cdn.app, name="cdn")


if __name__ == "__main__":
    app()
