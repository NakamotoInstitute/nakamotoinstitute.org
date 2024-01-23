import { urls } from "@/lib/urls";
import { RenderedItemsList, RenderedItemsListProps } from "./RenderedItemsList";
import { Author } from "@/lib/api/schemas/authors";
import Link from "next/link";

type AuthorLinksProps = Omit<
  RenderedItemsListProps<Author>,
  "items" | "renderItem"
> & {
  itemClassName?: string;
  authors: Author[];
};

export function AuthorsLinks({
  authors,
  locale,
  itemClassName,
  ...rest
}: AuthorLinksProps) {
  return (
    <RenderedItemsList
      items={authors}
      locale={locale}
      renderItem={(item) => (
        <Link
          className={itemClassName}
          key={item.slug}
          href={urls(locale).authors.detail(item.slug)}
        >
          {item.name}
        </Link>
      )}
      {...rest}
    />
  );
}
