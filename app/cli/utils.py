import click


def color_text(text, color="green"):
    return click.style(text, fg=color)


DONE = color_text("Done!")
