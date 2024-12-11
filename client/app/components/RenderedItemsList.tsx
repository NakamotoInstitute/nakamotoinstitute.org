import { ElementType, Fragment } from "react";

import { formatListWithPlaceholders } from "@/utils/strings";

type RenderFunction<T> = (item: T, index: number) => React.ReactNode;

export type RenderedItemsListProps<T> = {
  as?: ElementType;
  items: T[];
  renderItem: RenderFunction<T>;
  className?: string;
  options?: Intl.ListFormatOptions;
  locale: Locale;
};

export function RenderedItemsList<T = unknown>({
  as: WrapperComponent = "p",
  items,
  renderItem,
  className,
  options,
  locale,
}: RenderedItemsListProps<T>) {
  const formattedList = formatListWithPlaceholders(items, locale, options);
  const parts = formattedList.split(/%%\d+%%/);

  return (
    <WrapperComponent className={className}>
      {parts.map((part, index) => (
        <Fragment key={index}>
          {part}
          {index < items.length && renderItem(items[index], index)}
        </Fragment>
      ))}
    </WrapperComponent>
  );
}
