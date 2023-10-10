from sni import cli, create_app
from sni.models import blog_post_authors

app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {"blog_post_authors": blog_post_authors}
