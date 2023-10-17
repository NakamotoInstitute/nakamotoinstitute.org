import ReactMarkdown, { Options } from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import remarkDefinitionList from "remark-definition-list";
import rehypeKatex from "rehype-katex";
import rehypeRaw from "rehype-raw";

type MarkdownProps = {
  className?: string;
  hasMath?: boolean;
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

export async function Markdown({
  className,
  children,
  hasMath,
  remarkPlugins,
  additionalRemarkPlugins = [],
  rehypePlugins,
  additionalRehypePlugins = [],
  remarkRehypeOptions = null,
}: MarkdownProps) {
  const defaultRemarkPlugins = [remarkGfm, remarkDefinitionList];
  if (hasMath) {
    defaultRemarkPlugins.push(remarkMath);
  }
  const mergedRemarkPlugins = remarkPlugins || [
    ...defaultRemarkPlugins,
    ...additionalRemarkPlugins,
  ];

  const defaultRehypePlugins = [rehypeKatex, rehypeRaw];
  const mergedRehypePlugins = rehypePlugins || [
    ...defaultRehypePlugins,
    ...additionalRehypePlugins,
  ];

  // Only include katex css if it is needed
  if (hasMath && mergedRehypePlugins.includes(rehypeKatex)) {
    await require("katex/dist/katex.min.css");
  }

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
