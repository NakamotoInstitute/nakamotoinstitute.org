import { EmailSource, ForumPostSource } from "@/lib/api";

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

export function formatEmailSource(source: EmailSource) {
  return {
    "bitcoin-list": "bitcoin-list",
    cryptography: "Cryptography Mailing List",
  }[source];
}

export function formatPostSource(source: ForumPostSource) {
  return {
    bitcointalk: "BitcoinTalk",
    p2pfoundation: "P2P Foundation",
  }[source];
}
