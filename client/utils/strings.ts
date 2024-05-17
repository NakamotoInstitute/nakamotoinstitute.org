import { EmailSource } from "@/lib/api/schemas/emails";
import { ForumPostSource } from "@/lib/api/schemas/posts";
import { CapitalizedLocale } from "@/types/i18n";

export function getNumericId(id: number | string) {
  return typeof id === "string" ? parseInt(id, 10) : id;
}

export function commafy(str: string) {
  const parts = str.split(".");
  parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  return parts.join(".");
}

export function formatListWithPlaceholders(
  items: unknown[],
  locale: Locale,
  options?: Intl.ListFormatOptions,
) {
  const placeholders = items.map((_, index) => `%%${index}%%`);
  const formatter = new Intl.ListFormat(locale, {
    style: "long",
    type: "conjunction",
    ...options,
  });

  return formatter.format(placeholders);
}

export function formatLocale(locale: Locale): CapitalizedLocale {
  if (locale.includes("-")) {
    const [lang, region] = locale.split("-");
    return `${lang}-${region.toUpperCase()}` as CapitalizedLocale;
  }
  return locale as CapitalizedLocale;
}

export function otherEmailSource(source: EmailSource) {
  return source === "cryptography" ? "bitcoin-list" : "cryptography";
}

export function formatEmailSource(source: EmailSource, short: boolean = false) {
  return {
    "bitcoin-list": "bitcoin-list",
    cryptography: short ? "Cryptography" : "Cryptography Mailing List",
  }[source];
}

export function otherForumPostSource(source: ForumPostSource) {
  return source === "bitcointalk" ? "p2pfoundation" : "bitcointalk";
}

export function formatPostSource(source: ForumPostSource) {
  return {
    bitcointalk: "BitcoinTalk",
    p2pfoundation: "P2P Foundation",
  }[source];
}
