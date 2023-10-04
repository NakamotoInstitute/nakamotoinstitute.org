import { urls } from "@/lib/urls";
import { LinkedItemsList, LinkedItemsListProps } from "./LinkedItemsList";
import { Author } from "@/lib/api/schemas";

type AuthorLinksProps = Omit<LinkedItemsListProps, "items" | "urlFunc"> & {
  authors: Author[];
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
