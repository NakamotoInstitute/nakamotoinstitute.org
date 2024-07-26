import clsx from "clsx";
import { TFunction } from "i18next";
import Link from "next/link";

import { ButtonLink } from "@/app/components/Button";
import { Chip } from "@/app/components/Chip";
import { Document, DocumentIndex } from "@/lib/api/schemas/library";
import { urls } from "@/lib/urls";

type DocFormatLinksProps = {
  t: TFunction<string, string>;
  locale: Locale;
  className?: string;
  doc: Document;
  classes?: { root?: string; link?: string };
};

export async function DocFormatLinks({
  t,
  locale,
  classes,
  className,
  doc,
}: DocFormatLinksProps) {
  const links: React.ReactNode[] = [];

  if (doc.entryNode) {
    links.push(
      <ButtonLink
        key="online"
        href={urls(locale).library.docNode(doc.slug, doc.entryNode.slug)}
        className={classes?.link}
      >
        {t("read_online")}
      </ButtonLink>,
    );
  }

  doc.formats?.forEach((format) =>
    links.push(
      <ButtonLink key={format.type} className={classes?.link} href={format.url}>
        {format.type === "epub" ? "ePub" : format.type.toUpperCase()}
      </ButtonLink>,
    ),
  );

  if (doc.external) {
    links.push(
      <ButtonLink key="link" href={doc.external} className={classes?.link}>
        {t("external_link")}
      </ButtonLink>,
    );
  }

  if (doc.purchaseLink) {
    links.push(
      <ButtonLink
        key="purchase"
        variant="secondary"
        href={doc.purchaseLink}
        className={classes?.link}
      >
        {t("buy_now")}
      </ButtonLink>,
    );
  }

  return links ? (
    <div className={clsx(className, classes?.root, "flex gap-4")}>{links}</div>
  ) : null;
}

type DocFormatChipsProps = {
  t: TFunction<string, string>;
  className?: string;
  doc: DocumentIndex;
};

export async function DocFormatChips({
  t,
  className,
  doc,
}: DocFormatChipsProps) {
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
    chips.push(<Chip key="link">{t("link")}</Chip>);
  }

  return chips ? (
    <div className={clsx(className, "flex gap-1")}>{chips}</div>
  ) : null;
}
