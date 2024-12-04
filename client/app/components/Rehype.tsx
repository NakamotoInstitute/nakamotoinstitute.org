import Script from "next/script";
import * as runtime from "react/jsx-runtime";
import rehypeMathjax from "rehype-mathjax/browser";
import rehypeParse from "rehype-parse";
import rehypeReact, { Options } from "rehype-react";
import { unified } from "unified";

type RehypeProps = {
  hasMath?: boolean;
  children: string;
};

export function Rehype({ hasMath, children }: RehypeProps) {
  const rehypeOptions: Options = {
    Fragment: runtime.Fragment,
    jsx: runtime.jsx,
    jsxs: runtime.jsxs,
  };

  const processor = unified().use(rehypeParse, { fragment: true });

  if (hasMath) {
    processor.use(rehypeMathjax);
  }

  processor.use(rehypeReact, rehypeOptions);

  const file = processor.processSync(children);

  return (
    <>
      {hasMath ? (
        <Script src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-mml-chtml.js" />
      ) : null}
      {file.result as React.ReactNode}
    </>
  );
}
