from app import cli, create_app, db

# from app.models import (
#     Author,
#     BlogPost,
#     BlogPostTranslation,
#     BlogSeries,
#     Category,
#     Doc,
#     Email,
#     EmailThread,
#     Episode,
#     Format,
#     ForumThread,
#     Language,
#     Post,
#     Price,
#     Quote,
#     QuoteCategory,
#     ResearchDoc,
#     Skeptic,
#     Translator,
# )

app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        # "Author": Author,
        # "BlogPost": BlogPost,
        # "BlogPostTransaction": BlogPostTranslation,
        # "BlogSeries": BlogSeries,
        # "Category": Category,
        # "Doc": Doc,
        # "Email": Email,
        # "EmailThread": EmailThread,
        # "Episode": Episode,
        # "Format": Format,
        # "ForumThread": ForumThread,
        # "Language": Language,
        # "Post": Post,
        # "Price": Price,
        # "Quote": Quote,
        # "QuoteCategory": QuoteCategory,
        # "ResearchDoc": ResearchDoc,
        # "Skeptic": Skeptic,
        # "Translator": Translator,
    }
