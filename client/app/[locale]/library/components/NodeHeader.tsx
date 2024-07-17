import { TFunction } from "i18next";

import { DocumentNode } from "@/lib/api/schemas/library";

type NodeHeaderProps = {
  t: TFunction<string, string>;
  locale: Locale;
  node: DocumentNode;
};

export async function NodeHeader({ t, locale, node }: NodeHeaderProps) {
  return (
    <>
      <header className="mx-auto mt-6 max-w-4xl text-center">
        {node.heading ? (
          <p className="text-2xl font-medium">{node.heading}</p>
        ) : null}
        <h1 className="mb-2 text-5xl font-medium">{node.title}</h1>
        {node.subheading ? (
          <p
            className="italic-regular-em mb-6 text-2xl italic"
            dangerouslySetInnerHTML={{ __html: node.subheading }}
          />
        ) : null}
      </header>
      <hr className="mx-auto my-6 w-12 border border-opacity-40" />
    </>
  );
}
