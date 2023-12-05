import { Granularity } from "@/lib/api/schemas/library";

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

export const formatDocDate = (
  locale: Locale,
  date: Date,
  granularity: Granularity,
) => {
  switch (granularity) {
    case "YEAR":
      return formatDate(locale, date, { year: "numeric" });

    case "MONTH":
      return formatDate(locale, date, { year: "numeric", month: "long" });

    case "DAY":
      return formatDate(locale, date);

    default:
      return "";
  }
};

export const formatTimeAttr = (date: Date, granularity: Granularity) => {
  const year = date.getUTCFullYear();

  switch (granularity) {
    case "DAY": {
      const month = String(date.getUTCMonth() + 1).padStart(2, "0");
      const day = String(date.getUTCDate()).padStart(2, "0");
      return `${year}-${month}-${day}`;
    }

    case "MONTH": {
      const month = String(date.getUTCMonth() + 1).padStart(2, "0");
      return `${year}-${month}`;
    }

    case "YEAR":
      return String(year);

    default:
      return "";
  }
};

export const calculateDayDifference = (date1: Date, date2: Date) => {
  const timeDifference = Math.abs(date2.getTime() - date1.getTime());
  const dayDifference = Math.ceil(timeDifference / (1000 * 3600 * 24));
  return dayDifference;
};
