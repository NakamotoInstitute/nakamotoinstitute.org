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
