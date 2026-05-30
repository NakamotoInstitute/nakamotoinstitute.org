/**
 * Render a `ts_headline` snippet safely: only the server-emitted <mark> markup is
 * turned into elements; everything else is escaped as plain text (NO
 * dangerouslySetInnerHTML). Shared by the /search page and the command palette.
 *
 * `<mark>` is styled editorially (cardinal + bold, no glaring yellow) per A16.
 */
type SearchHighlightProps = { snippet: string };

// ts_headline returns the indexed content verbatim, so snippets can carry HTML
// entities from the source (e.g. quoted email lines written as "&gt;"). Decode
// the common ones so they read naturally. Stays XSS-safe: the decoded text is
// rendered as React children (re-escaped on output), never as raw HTML.
function decodeEntities(text: string): string {
  return text
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#0*39;|&apos;/g, "'")
    .replace(/&nbsp;/g, " ")
    .replace(/&amp;/g, "&");
}

export function SearchHighlight({ snippet }: SearchHighlightProps) {
  const parts = snippet.split(/(<mark>.*?<\/mark>)/g);
  return (
    <>
      {parts.map((part, i) => {
        const match = part.match(/^<mark>(.*?)<\/mark>$/s);
        return match ? (
          <mark key={i} className="bg-transparent font-bold text-cardinal">
            {decodeEntities(match[1])}
          </mark>
        ) : (
          <span key={i}>{decodeEntities(part)}</span>
        );
      })}
    </>
  );
}
