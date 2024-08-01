import { DocumentNode } from "@/lib/api/schemas/library";

type NodeHeaderProps = {
  node: DocumentNode;
  hr: "middle" | "bottom" | "both";
};

export async function NodeHeader({ node, hr }: NodeHeaderProps) {
  return (
    <>
      <header className="mx-auto mt-6 max-w-4xl text-center">
        {node.heading ? (
          <p className="mb-4 text-center text-2xl font-medium md:text-3xl">
            {node.heading}
          </p>
        ) : null}
        {hr === "middle" || hr === "both" ? (
          <hr className="mx-auto my-6 w-12 border border-opacity-40" />
        ) : null}
        <h1 className="mb-2.5 text-4xl font-semibold leading-[1.1] md:mb-4 md:text-7xl md:font-medium">
          {node.title}
        </h1>

        {node.subheading ? (
          <p
            className="mx-auto mb-4 max-w-prose text-xl font-bold small-caps md:mb-6 md:text-2xl"
            dangerouslySetInnerHTML={{ __html: node.subheading }}
          />
        ) : null}
      </header>
      {hr === "bottom" || hr === "both" ? (
        <hr className="mx-auto my-6 w-12 border border-opacity-40" />
      ) : null}
    </>
  );
}
