import { ElementType, Fragment } from "react";
import Link from "next/link";
import { formatListWithPlaceholders } from "@/utils/strings";

export type LinkedItemsListProps = {
  as?: ElementType;
  items: { name: string; slug: string }[];
  urlFunc: (locale: Locale, slug: string) => string;
  classes?: {
    root?: string;
    link?: string;
  };
  options?: Intl.ListFormatOptions;
  locale: Locale;
};

export function LinkedItemsList({
  as: WrapperComponent = "p",
  classes,
  urlFunc,
  items,
  options,
  locale,
}: LinkedItemsListProps) {
  const formattedList = formatListWithPlaceholders(items, locale, {
    ...options,
  });
  const parts = formattedList.split(/%%\d+%%/);
  return (
    <WrapperComponent className={classes?.root}>
      {parts.map((part, index) => (
        <Fragment key={index}>
          {part}
          {index < items.length ? (
            <Link
              key={items[index].slug}
              className={classes?.link}
              href={urlFunc(locale, items[index].slug)}
            >
              {items[index].name}
            </Link>
          ) : null}
        </Fragment>
      ))}
    </WrapperComponent>
  );
}
