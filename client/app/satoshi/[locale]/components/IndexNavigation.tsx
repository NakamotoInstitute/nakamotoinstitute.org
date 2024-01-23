import clsx from "clsx";
import Link from "next/link";

export type IndexLink = {
  label: string;
  href: string;
};

type IndexLinkWithSublink = IndexLink & {
  sublink?: IndexLink;
};

export type IndexLinks = {
  main: IndexLink;
  left: IndexLinkWithSublink;
  right: IndexLinkWithSublink;
};

type IndexNavigationProps = {
  links: IndexLinks;
  reverse?: boolean;
};

export const IndexNavigation = ({
  links: { main, left, right },
  reverse = false,
}: IndexNavigationProps) => {
  const renderLink = (link: IndexLink) =>
    link.href ? (
      <Link href={link.href}>{link.label}</Link>
    ) : (
      <span>{link.label}</span>
    );

  return (
    <div className="grid grid-cols-2 grid-rows-2 gap-y-2 text-center">
      <div className={clsx("col-span-2", reverse && "order-2")}>
        {renderLink(main)}
      </div>
      <div className="border-r border-gray-400 pr-2 text-right">
        {renderLink(left)}
        {left.sublink ? (
          <>
            {" ("}
            {renderLink(left.sublink)}
            {")"}
          </>
        ) : null}
      </div>
      <div className="pl-2 text-left">
        {renderLink(right)}
        {right.sublink ? (
          <>
            {" ("}
            {renderLink(right.sublink)}
            {")"}
          </>
        ) : null}
      </div>
    </div>
  );
};
