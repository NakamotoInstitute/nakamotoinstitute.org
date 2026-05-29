/**
 * Render a `ts_headline` snippet safely: only the server-emitted <mark> markup is
 * turned into elements; everything else is escaped as plain text (NO
 * dangerouslySetInnerHTML). Shared by the /search page and the command palette.
 *
 * `<mark>` is styled editorially (cardinal + bold, no glaring yellow) per A16.
 */
type SearchHighlightProps = { snippet: string };

export function SearchHighlight({ snippet }: SearchHighlightProps) {
  const parts = snippet.split(/(<mark>.*?<\/mark>)/g);
  return (
    <>
      {parts.map((part, i) => {
        const match = part.match(/^<mark>(.*?)<\/mark>$/s);
        return match ? (
          <mark key={i} className="bg-transparent font-bold text-cardinal">
            {match[1]}
          </mark>
        ) : (
          <span key={i}>{part}</span>
        );
      })}
    </>
  );
}
