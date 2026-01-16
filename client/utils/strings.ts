import { EmailSource, ForumPostSource } from "@/lib/api";
import { CapitalizedLocale } from "@/types/i18n";

export function getNumericId(id: number | string) {
  return typeof id === "string" ? parseInt(id, 10) : id;
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

export function formatEmailSource(source: EmailSource, short: boolean = false) {
  return {
    "bitcoin-list": "bitcoin-list",
    cryptography: short ? "Cryptography" : "Cryptography Mailing List",
    "p2p-research": short ? "p2p-research" : "P2P Research List",
  }[source];
}

export function formatPostSource(source: ForumPostSource) {
  return {
    bitcointalk: "BitcoinTalk",
    p2pfoundation: "P2P Foundation",
  }[source];
}
