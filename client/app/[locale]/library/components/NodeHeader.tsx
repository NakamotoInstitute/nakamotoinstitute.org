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
          <p className="mb-2 text-center text-2xl font-bold small-caps md:mb-4 md:text-4xl">
            {node.heading}
          </p>
        ) : null}
        {hr === "middle" || hr === "both" ? (
          <hr className="mx-auto my-6 w-12 border border-opacity-40" />
        ) : null}
        <h1 className="mb-4 text-4xl font-medium leading-[1.1] md:mb-6 md:text-7xl">
          {node.title}
        </h1>

        {node.subheading ? (
          <p
            className="italic-regular-em mb-4 text-xl font-semibold italic md:mb-6 md:text-2xl"
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
