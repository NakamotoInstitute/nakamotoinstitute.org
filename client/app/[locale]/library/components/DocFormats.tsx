import clsx from "clsx";
import { TFunction } from "i18next";

import { ButtonLink, ButtonLinkProps } from "@/app/components/Button";
import { Chip } from "@/app/components/Chip";
import { Document, DocumentIndex } from "@/lib/api/schemas/library";
import { urls } from "@/lib/urls";

async function DocFormatButtonLink({ className, ...rest }: ButtonLinkProps) {
  return <ButtonLink className={clsx(className, "w-28")} {...rest} />;
}

type DocFormatLinkProps = {
  t: TFunction<string, string>;
  locale: Locale;
  doc: Document;
  buttonClassName?: string;
};

export function getDocFormatLinks({
  t,
  locale,
  doc,
  buttonClassName,
}: DocFormatLinkProps): React.ReactNode[] {
  const links: React.ReactNode[] = [];

  if (doc.entryNode) {
    links.push(
      <DocFormatButtonLink
        key="online"
        href={urls(locale).library.docNode(doc.slug, doc.entryNode.slug)}
        className={buttonClassName}
      >
        {t("read_online")}
      </DocFormatButtonLink>,
    );
  }

  doc.formats?.forEach((format) =>
    links.push(
      <DocFormatButtonLink
        key={format.volume ? `${format.type}-${format.volume}` : format.type}
        className={buttonClassName}
        href={format.url}
      >
        {format.type === "epub" ? "ePub" : format.type.toUpperCase()}
        {format.volume ? ` (Vol. ${format.volume})` : ""}
      </DocFormatButtonLink>,
    ),
  );

  if (doc.external) {
    links.push(
      <DocFormatButtonLink
        key="link"
        href={doc.external}
        className={buttonClassName}
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
        className={buttonClassName}
      >
        {t("buy_now")}
      </DocFormatButtonLink>,
    );
  }

  return links;
}

type DocFormatLinksBoxProps = {
  links: React.ReactNode[];
  className?: string;
  border?: boolean;
};

export function DocFormatLinksContainer({
  links,
  className,
  border = false,
}: DocFormatLinksBoxProps) {
  if (links.length === 0) return null;

  return (
    <>
      <div className={clsx(className, "flex justify-center gap-4")}>
        {links}
      </div>
      {border && <hr className="mx-auto my-6 w-12" />}
    </>
  );
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

  const formatTypes = new Set(doc.formats?.map((f) => f.type));
  formatTypes.forEach((type) =>
    chips.push(
      <Chip key={type}>{type === "epub" ? "ePub" : type.toUpperCase()}</Chip>,
    ),
  );

  if (doc.external) {
    chips.push(<Chip key="link">{t("link")}</Chip>);
  }

  return chips ? (
    <div className={clsx(className, "flex gap-1")}>{chips}</div>
  ) : null;
}
