import clsx from "clsx";
import Link from "next/link";

import { Chip } from "@/app/components/Chip";
import { Document, DocumentIndex } from "@/lib/api/schemas/library";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";

type DocFormatLinksProps = {
  locale: Locale;
  className?: string;
  doc: Document;
  classes?: { root?: string; link?: string };
};

export async function DocFormatLinks({
  classes,
  className,
  doc,
  locale,
}: DocFormatLinksProps) {
  const { t } = await i18nTranslation(locale);
  const links: React.ReactNode[] = [];

  doc.formats?.forEach((format) =>
    links.push(
      <Link key={format.type} className={classes?.link} href={format.url}>
        {format.type === "epub" ? "ePub" : format.type.toUpperCase()}
      </Link>,
    ),
  );

  if (doc.external) {
    links.push(
      <Link key="link" href={doc.external} className={classes?.link}>
        {t("External link")}
      </Link>,
    );
  }

  return links ? (
    <div className={clsx(className, classes?.root, "flex gap-3")}>{links}</div>
  ) : null;
}

type DocFormatChipsProps = {
  locale: Locale;
  className?: string;
  doc: DocumentIndex;
};

export async function DocFormatChips({
  locale,
  className,
  doc,
}: DocFormatChipsProps) {
  const { t } = await i18nTranslation(locale);
  const chips: React.ReactNode[] = [];

  if (doc.hasContent) {
    chips.push(<Chip key="html">HTML</Chip>);
  }

  doc.formats?.forEach((format) =>
    chips.push(
      <Chip key={format.type}>
        {format.type === "epub" ? "ePub" : format.type.toUpperCase()}
      </Chip>,
    ),
  );

  if (doc.external) {
    chips.push(<Chip key="link">{t("Link")}</Chip>);
  }

  return chips ? (
    <div className={clsx(className, "flex gap-1")}>{chips}</div>
  ) : null;
}
