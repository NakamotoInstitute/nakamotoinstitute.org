import Link from "next/link";
import { ElementType } from "react";

import { RenderedItemsList } from "@/app/components/RenderedItemsList";
import { languages } from "@/i18n";
import { TranslationSchema } from "@/lib/api";

type TranslationLinksProps = {
  as?: ElementType;
  locale: Locale;
  translations: TranslationSchema[];
  urlFunc: (item: TranslationSchema) => string;
};

export const TranslationLinks = ({
  as = "span",
  locale,
  translations,
  urlFunc,
}: TranslationLinksProps) => {
  return (
    <RenderedItemsList
      as={as}
      locale={locale}
      items={translations}
      renderItem={(item) => {
        const name = languages[item.locale];
        return <Link href={urlFunc(item)}>{name}</Link>;
      }}
    />
  );
};
