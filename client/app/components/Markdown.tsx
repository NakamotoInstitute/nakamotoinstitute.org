import clsx from "clsx";
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
        remarkPlugins={mergedRemarkPlugins}
        rehypePlugins={mergedRehypePlugins}
        remarkRehypeOptions={mergedRemarkRehypeOptions}
        components={{
          a: ({
            children,
            href,
            ref,
            ...rest
          }: React.ComponentPropsWithRef<"a">) => {
            if (href?.startsWith("/")) {
              return (
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

export type MarkdownContentProps = {
  className?: string;
} & MarkdownProps;

export async function MarkdownContent({
  className,
  ...props
}: MarkdownContentProps) {
  return (
    <div className={className}>
      <Markdown {...props} />
    </div>
  );
}

export async function PageContent({
  className,
  ...props
}: MarkdownContentProps) {
  return (
    <MarkdownContent
      className={clsx(
        "[&_h2]:mb-2 [&_h2]:text-3xl [&_h2]:font-medium",
        "[&_p]:mb-4",
        "[&_a]:text-cardinal [&_a]:hover:underline",
        "[&_figure]:border-dark [&_figure]:border-l [&_figure]:border-dashed",
        "[&_figure_blockquote]:px-4 [&_figure_blockquote]:italic",
        "[&_figure_figcaption]:small-caps [&_figure_figcaption]:mt-2 [&_figure_figcaption]:px-4 [&_figure_figcaption]:font-medium",
        className,
      )}
      {...props}
    />
  );
}
