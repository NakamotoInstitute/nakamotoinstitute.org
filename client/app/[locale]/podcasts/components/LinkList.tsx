import clsx from "clsx";
import Link from "next/link";

type Link = {
  href: string;
  label: string;
};

type LinkListProps = {
  title: string;
  links: (Link | false)[];
  className?: string;
};

export function LinkList({ title, links, className }: LinkListProps) {
  return (
    <div
      className={clsx(
        "flex flex-col items-baseline md:flex-row md:gap-2",
        className,
      )}
    >
      <p className="font-bold">{title}:</p>
      <ul className="flex flex-col md:flex-row md:items-center">
        {links
          .filter((link): link is Link => Boolean(link))
          .map((link, i) => (
            <li
              key={i}
              className="before:text-taupe first:before:mx-0 first:before:content-none md:before:mx-2 md:before:content-['•']"
            >
              <Link href={link.href} className="underline">
                {link.label}
              </Link>
            </li>
          ))}
      </ul>
    </div>
  );
}
