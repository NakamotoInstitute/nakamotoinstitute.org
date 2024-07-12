import Link from "next/link";

export type Breadcrumb = {
  label: string;
  href: string;
};

export type Breadcrumbs = [Breadcrumb, Breadcrumb, ...Breadcrumb[]];

export type BreadcrumbsProps = {
  breadcrumbs: Breadcrumbs;
};

export async function Breadcrumbs({ breadcrumbs }: BreadcrumbsProps) {
  return (
    <nav
      aria-label="breadcrumb"
      className="border-b-1 border-dashed border-dark py-3"
    >
      <ol className="flex justify-center gap-x-2">
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
    </nav>
  );
}
