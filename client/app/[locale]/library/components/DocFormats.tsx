import { ReactNode } from "react";
import clsx from "clsx";
import { Chip } from "@/app/components";
import { DocumentIndex } from "@/lib/api/schemas";
import { i18nTranslation } from "@/lib/i18n";

export async function DocFormats({
  locale,
  className,
  doc,
}: {
  locale: Locale;
  className?: string;
  doc: DocumentIndex;
}) {
  const { t } = await i18nTranslation(locale);
  const chips: ReactNode[] = [];

  if (doc.hasContent) {
    chips.push(<Chip key="html">HTML</Chip>);
  }

  doc.formats?.forEach((format) =>
    chips.push(
      <Chip key={format}>
        {format === "epub" ? "ePub" : format.toUpperCase()}
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
