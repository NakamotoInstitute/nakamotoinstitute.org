import {
  PluggableList,
  ReactMarkdown,
  ReactMarkdownOptions,
} from "react-markdown/lib/react-markdown";
import remarkGfm from "remark-gfm";
import remarkDefinitionList from "remark-definition-list";
import rehypeRaw from "rehype-raw";

type MarkdownProps = {
  className?: string;
  children: string;
  remarkPlugins?: PluggableList;
  rehypePlugins?: PluggableList;
  remarkRehypeOptions?: ReactMarkdownOptions["remarkRehypeOptions"];
};

export function Markdown({
  className,
  children,
  remarkPlugins,
  rehypePlugins,
  remarkRehypeOptions = { clobberPrefix: undefined },
}: MarkdownProps) {
  const { clobberPrefix, ...otherOptions } = remarkRehypeOptions;
  return (
    <ReactMarkdown
      className={className}
      remarkPlugins={remarkPlugins ?? [remarkGfm, remarkDefinitionList]}
      rehypePlugins={rehypePlugins ?? [rehypeRaw]}
      remarkRehypeOptions={{
        clobberPrefix: clobberPrefix ?? "",
        ...otherOptions,
      }}
    >
      {children}
    </ReactMarkdown>
  );
}
