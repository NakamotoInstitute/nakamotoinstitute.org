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
