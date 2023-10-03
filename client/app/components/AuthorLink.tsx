import { urls } from "@/lib/urls";
import { LinkedItemsList, LinkedItemsListProps } from "./LinkedItemsList";
import Link from "next/link";
import { AuthorData } from "@/lib/api/schemas";

type AuthorLinkProps = {
  locale: Locale;
  author: AuthorData;
};

export function AuthorLink({ author, locale }: AuthorLinkProps) {
  return (
    <Link href={urls(locale).authors.detail(author.slug)}>{author.name}</Link>
  );
}

type AuthorLinksProps = Omit<LinkedItemsListProps, "items" | "urlFunc"> & {
  authors: AuthorData[];
};

export function AuthorsLinks({ authors, ...rest }: AuthorLinksProps) {
  return (
    <LinkedItemsList
      items={authors}
      urlFunc={(_locale, _slug) => urls(_locale).authors.detail(_slug)}
      {...rest}
    />
  );
}
