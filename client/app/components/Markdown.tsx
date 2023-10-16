import ReactMarkdown, { Options } from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkDefinitionList from "remark-definition-list";
import rehypeRaw from "rehype-raw";

type MarkdownProps = {
  className?: string;
  children: string;
  remarkPlugins?: Options["remarkPlugins"];
  additionalRemarkPlugins?: NonNullable<Options["remarkPlugins"]>;
  rehypePlugins?: Options["rehypePlugins"];
  additionalRehypePlugins?: NonNullable<Options["rehypePlugins"]>;
  remarkRehypeOptions?:
    | Partial<Options["remarkRehypeOptions"]>
    | null
    | undefined;
};

export function Markdown({
  className,
  children,
  remarkPlugins,
  additionalRemarkPlugins = [],
  rehypePlugins,
  additionalRehypePlugins = [],
  remarkRehypeOptions = null,
}: MarkdownProps) {
  const defaultRemarkPlugins = [remarkGfm, remarkDefinitionList];
  const mergedRemarkPlugins = remarkPlugins || [
    ...defaultRemarkPlugins,
    ...additionalRemarkPlugins,
  ];

  const defaultRehypePlugins = [rehypeRaw];
  const mergedRehypePlugins = rehypePlugins || [
    ...defaultRehypePlugins,
    ...additionalRehypePlugins,
  ];

  const defaultRemarkRehypeOptions = {
    clobberPrefix: null,
  };

  const mergedRemarkRehypeOptions = {
    ...defaultRemarkRehypeOptions,
    ...remarkRehypeOptions,
  };

  return (
    <ReactMarkdown
      className={className}
      remarkPlugins={mergedRemarkPlugins}
      rehypePlugins={mergedRehypePlugins}
      remarkRehypeOptions={mergedRemarkRehypeOptions}
    >
      {children}
    </ReactMarkdown>
  );
}
