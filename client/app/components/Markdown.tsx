import Link from "next/link";
import Script from "next/script";
import ReactMarkdown, { Options } from "react-markdown";
import rehypeMathjax from "rehype-mathjax/browser";
import rehypeRaw from "rehype-raw";
import remarkDefinitionList from "remark-definition-list";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";

import { toFullUrl } from "@/lib/urls";

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
  const defaultRemarkPlugins: Options["remarkPlugins"] = [
    remarkGfm,
    remarkDefinitionList,
  ];
  if (hasMath) {
    defaultRemarkPlugins.push(remarkMath);
  }
  const mergedRemarkPlugins = remarkPlugins || [
    ...defaultRemarkPlugins,
    ...additionalRemarkPlugins,
  ];

  const defaultRehypePlugins: Options["rehypePlugins"] = [rehypeRaw];
  if (hasMath) {
    defaultRehypePlugins.unshift(rehypeMathjax);
  }
  const mergedRehypePlugins = rehypePlugins || [
    ...defaultRehypePlugins,
    ...additionalRehypePlugins,
  ];

  const defaultRemarkRehypeOptions: Partial<Options["remarkRehypeOptions"]> = {
    clobberPrefix: null,
  };

  const mergedRemarkRehypeOptions = {
    ...defaultRemarkRehypeOptions,
    ...remarkRehypeOptions,
  };

  return (
    <>
      {hasMath ? (
        <Script src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-mml-chtml.js" />
      ) : null}
      <ReactMarkdown
        className={className}
        remarkPlugins={mergedRemarkPlugins}
        rehypePlugins={mergedRehypePlugins}
        remarkRehypeOptions={mergedRemarkRehypeOptions}
        components={{
          a(props) {
            const { children, href, ref, ...rest } = props;
            if (href?.startsWith("/")) {
              return (
                // Todo: figure out how to forward this ref
                <Link href={toFullUrl(href)} {...rest}>
                  {children}
                </Link>
              );
            }
            return (
              <a ref={ref} href={href} {...rest}>
                {children}
              </a>
            );
          },
        }}
      >
        {children}
      </ReactMarkdown>
    </>
  );
}
