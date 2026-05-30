import clsx from "clsx";
import Link from "next/link";

import { Arrow } from "@/app/components/Arrow";
import { focusUnderline } from "@/lib/focusRing";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { urls } from "@/lib/urls";

// Category tabs that survive a round-trip to the results page (mirrors the
// /search page's CATEGORIES; authors is intentionally excluded from search).
const SEARCH_TABS = ["satoshi", "library", "mempool", "podcasts"];

// searchParams values are string | string[] | undefined; take the first.
type SearchParam = string | string[] | undefined;
const first = (value: SearchParam) =>
  Array.isArray(value) ? value[0] : value;

type BackToSearchProps = {
  locale: Locale;
  from?: SearchParam;
  q?: SearchParam;
  tab?: SearchParam;
};

/**
 * "← Back to results" link shown on a detail page only when it was reached from
 * the /search results page (?from=search&q=…). Server-rendered and JS-free; it
 * returns to the full results page for the same query (and category tab).
 */
export async function BackToSearch({ locale, from, q, tab }: BackToSearchProps) {
  const query = first(q)?.trim();
  const tabValue = first(tab);
  if (first(from) !== "search" || !query) {
    return null;
  }

  const { t } = await i18nTranslation(locale);
  const href = urls(locale).search({
    q: query,
    tab: tabValue && SEARCH_TABS.includes(tabValue) ? tabValue : undefined,
  });

  return (
    <Link
      href={href}
      className={clsx(
        "group text-cardinal small-caps mb-4 inline-flex items-center gap-x-1.5 text-sm hover:underline",
        focusUnderline,
      )}
    >
      <Arrow direction="back" className="rtl:rotate-180" />
      {t("search_back_to_results", { query })}
    </Link>
  );
}
