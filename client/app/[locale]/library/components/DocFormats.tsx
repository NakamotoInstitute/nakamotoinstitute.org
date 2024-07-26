import clsx from "clsx";
import { TFunction } from "i18next";

import { ButtonLink, ButtonLinkProps } from "@/app/components/Button";
import { Chip } from "@/app/components/Chip";
import { Document, DocumentIndex } from "@/lib/api/schemas/library";
import { urls } from "@/lib/urls";

async function DocFormatButtonLink({ className, ...rest }: ButtonLinkProps) {
  return <ButtonLink className={clsx(className, "w-28")} {...rest} />;
}

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

  const buttonClasses = clsx(classes?.link, "w-28");

  if (doc.entryNode) {
    links.push(
      <DocFormatButtonLink
        key="online"
        href={urls(locale).library.docNode(doc.slug, doc.entryNode.slug)}
        className={buttonClasses}
      >
        {t("read_online")}
      </DocFormatButtonLink>,
    );
  }

  doc.formats?.forEach((format) =>
    links.push(
      <DocFormatButtonLink
        key={format.type}
        className={buttonClasses}
        href={format.url}
      >
        {format.type === "epub" ? "ePub" : format.type.toUpperCase()}
      </DocFormatButtonLink>,
    ),
  );

  if (doc.external) {
    links.push(
      <DocFormatButtonLink
        key="link"
        href={doc.external}
        className={buttonClasses}
      >
        {t("external_link")}
      </DocFormatButtonLink>,
    );
  }

  if (doc.purchaseLink) {
    links.push(
      <DocFormatButtonLink
        key="purchase"
        variant="secondary"
        href={doc.purchaseLink}
        className={buttonClasses}
      >
        {t("buy_now")}
      </DocFormatButtonLink>,
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
