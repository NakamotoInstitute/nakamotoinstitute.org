export const formatDate = (
  locale: Locale,
  date: Date,
  options: Intl.DateTimeFormatOptions = {
    dateStyle: "long",
  },
) => {
  return Intl.DateTimeFormat(locale, {
    timeZone: "UTC",
    ...options,
  }).format(date);
};

export const formatDateRange = (
  locale: Locale,
  startDate: Date,
  endDate: Date,
  options: Intl.DateTimeFormatOptions = {
    year: "numeric",
    month: "long",
    day: "numeric",
  },
) => {
  return Intl.DateTimeFormat(locale, {
    timeZone: "UTC",
    ...options,
  }).formatRange(startDate, endDate);
};
