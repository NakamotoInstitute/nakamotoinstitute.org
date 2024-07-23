import Link from "next/link";

import { formatDate } from "@/utils/dates";

type ContentListingProps = {
  locale: Locale;
  label: string;
  href: string;
  date: Date;
};

export function ContentListing({
  locale,
  label,
  href,
  date,
}: ContentListingProps) {
  return (
    <article className="border-b border-dashed border-taupe-light py-5">
      <h3 className="text-xl font-bold">
        <Link className="text-cardinal hover:underline" href={href}>
          {label}
        </Link>
      </h3>
      <p className="small-caps">
        {formatDate(locale, date, {
          dateStyle: "medium",
          timeStyle: "long",
          hourCycle: "h24",
        })}
      </p>
    </article>
  );
}
