import clsx from "clsx";
import Link from "next/link";

type ListItem = {
  name: string;
  slug: string;
};

type ListColumnProps = {
  items: ListItem[];
  last?: boolean;
  equal?: boolean;
  hrefFunc: (slug: string) => string;
};

function LinkColumn({
  items,
  hrefFunc,
  last = false,
  equal = true,
}: ListColumnProps) {
  return (
    <ul className="md:w-1/2">
      {items.map((item) => (
        <li
          className={clsx(
            "border-b border-dashed border-taupe-light py-2",
            !last
              ? "md:last:border-b-0"
              : equal
                ? "last:border-b-0"
                : "last:border-b-0 md:last:border-b",
          )}
          key={item.slug}
        >
          <Link
            className="text-cardinal hover:underline"
            href={hrefFunc(item.slug)}
          >
            {item.name}
          </Link>
        </li>
      ))}
    </ul>
  );
}

type ListColumnLayoutProps = {
  items: { name: string; slug: string }[];
  hrefFunc: (slug: string) => string;
};

export function ListColumnLayout({ hrefFunc, items }: ListColumnLayoutProps) {
  const halfLength = Math.ceil(items.length / 2);
  const firstColumn = items.slice(0, halfLength);
  const secondColumn = items.slice(halfLength);

  return (
    <section className="my-4 flex flex-col gap-x-6 border-b border-t border-dashed border-taupe-light md:flex-row">
      <LinkColumn items={firstColumn} hrefFunc={hrefFunc} />
      <LinkColumn
        items={secondColumn}
        hrefFunc={hrefFunc}
        last
        equal={firstColumn.length === secondColumn.length}
      />
    </section>
  );
}
