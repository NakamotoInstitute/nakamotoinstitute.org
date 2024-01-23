import { ElementType } from "react";
import Link from "next/link";
import languages from "@/locales/languages.json";
import { RenderedItemsList } from "@/app/components/RenderedItemsList";
import { TranslationData } from "@/lib/api/schemas/shared";

type TranslationLinksProps = {
  as?: ElementType;
  locale: Locale;
  translations: TranslationData[];
  urlFunc: (item: TranslationData) => string;
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
        const language = languages.find((lang) => lang.code === item.locale);
        return <Link href={urlFunc(item)}>{language?.name}</Link>;
      }}
    />
  );
};
