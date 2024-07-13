import Link from "next/link";

import { ReturnButton } from "./ReturnButton";

export type Breadcrumb = {
  label: string;
  href: string;
};

export type Breadcrumbs = [Breadcrumb, Breadcrumb, ...Breadcrumb[]];

export type BreadcrumbsProps = {
  breadcrumbs: Breadcrumbs;
};

export async function Breadcrumbs({ breadcrumbs }: BreadcrumbsProps) {
  const returnCrumb = breadcrumbs[breadcrumbs.length - 2];
  return (
    <nav
      aria-label="breadcrumb"
      className="border-b-1 border-dashed border-dark py-3"
    >
      <ol className="hidden justify-center gap-x-2 md:flex">
        {breadcrumbs.map((breadcrumb, index) => {
          return (
            <li key={index} className="flex items-center gap-x-2">
              {index === 0 ? (
                <Link className="text-cardinal" href={breadcrumb.href}>
                  {breadcrumb.label}
                </Link>
              ) : (
                <>
                  <span className="text-taupe">/</span>
                  <Link href={breadcrumb.href}>{breadcrumb.label}</Link>
                </>
              )}
            </li>
          );
        })}
      </ol>
      <ReturnButton className="mx-auto w-fit md:hidden" {...returnCrumb} />
    </nav>
  );
}
