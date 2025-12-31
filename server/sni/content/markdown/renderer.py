from collections.abc import Sequence
from typing import cast

import yaml
from bs4 import BeautifulSoup
from markdown_it import MarkdownIt
from markdown_it.renderer import RendererHTML, RendererProtocol
from markdown_it.token import Token
from markdown_it.utils import EnvType, OptionsDict
from mdit_py_plugins.deflist import deflist_plugin
from mdit_py_plugins.dollarmath import dollarmath_plugin
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.subscript import sub_plugin
from pygments import highlight as pygments_highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

from sni.config import settings


def highlight_code(code: str, lang: str, attrs: str) -> str:
    """
    Highlight code blocks using Pygments with standard classes.
    The client will style these classes with Tailwind.
    """
    if not lang:
        return f"<pre><code>{code}</code></pre>"

    pre_class = f"hl-code language-{lang}"

    try:
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter(nowrap=True, classprefix="")
        highlighted_code = pygments_highlight(code, lexer, formatter)
    except ClassNotFound:
        # Fallback for unknown languages
        highlighted_code = code

    return f'<pre class="{pre_class}"><code>{highlighted_code}</code></pre>'


def render_math_inline(
    self: RendererProtocol,
    tokens: Sequence[Token],
    idx: int,
    options: OptionsDict,
    env: EnvType,
) -> str:
    return f"<span class='language-math math-inline'>{tokens[idx].content}</span>"


def render_math_block(
    self: RendererProtocol,
    tokens: Sequence[Token],
    idx: int,
    options: OptionsDict,
    env: EnvType,
) -> str:
    return f'<div class="language-math math-display">\n{tokens[idx].content}\n</div>\n'


class SNIMarkdownRenderer(RendererHTML):
    """
    Custom Markdown Renderer that can handle front matter.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._front_matter: dict | None = None

    def front_matter(self, tokens, idx, options, env) -> str:
        self._front_matter = yaml.safe_load(tokens[idx].content)
        return self.renderToken(tokens, idx, options, env)


class MDRenderer:
    """
    Class to process Markdown files and convert them to HTML.
    Handles front matter using YAML.
    """

    @classmethod
    def process_html(cls, html_content):
        soup = BeautifulSoup(html_content, "html.parser")

        for img in soup.find_all("img"):
            src = img.get("src")
            if src and src.startswith("/static"):
                img["src"] = src.replace("/static", settings.CDN_BASE_URL)

        for a in soup.find_all("a"):
            href = a.get("href")
            if href and href.startswith("/static"):
                a["href"] = href.replace("/static", settings.CDN_BASE_URL)
            elif href and href.startswith("/satoshi"):
                a["href"] = href.replace("/satoshi", settings.SATOSHI_URL)

        return str(soup)

    @classmethod
    def process_md(cls, md_file_path: str) -> tuple[dict | None, str, str]:
        md = (
            MarkdownIt(
                "commonmark",
                {
                    "breaks": False,
                    "html": True,
                    "typographer": True,
                    "highlight": highlight_code,
                },
                renderer_cls=SNIMarkdownRenderer,
            )
            .enable(["replacements", "smartquotes"])
            .use(front_matter_plugin)
            .use(sub_plugin)
            .use(footnote_plugin)
            .use(deflist_plugin)
            .use(dollarmath_plugin)
        )

        md.add_render_rule("math_inline", render_math_inline)
        md.add_render_rule("math_block", render_math_block)

        file_content = cls._get_file_content(md_file_path)
        html_content = md.render(file_content).strip()
        processed_html_content = cls.process_html(html_content)

        renderer = cast(SNIMarkdownRenderer, md.renderer)

        return renderer._front_matter, processed_html_content, file_content

    @classmethod
    def _get_file_content(cls, md_file_path: str) -> str:
        with open(md_file_path, encoding="utf-8") as reader:
            return reader.read()
