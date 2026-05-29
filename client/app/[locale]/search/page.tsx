import clsx from "clsx";
import { TFunction } from "i18next";
import { Metadata } from "next";
import Link from "next/link";

import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import { SearchHighlight } from "@/app/components/SearchHighlight";
import { locales } from "@/i18n";
import { CountsByCategory, SearchResult, api } from "@/lib/api";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { searchResultHref } from "@/lib/searchResultHref";
import { urls } from "@/lib/urls";
import { formatDate } from "@/utils/dates";

export const dynamicParams = false;

const CATEGORIES = [
  "satoshi",
  "library",
  "mempool",
  "authors",
  "podcasts",
] as const;

type Category = (typeof CATEGORIES)[number];

const CATEGORY_LABEL_KEYS = {
  satoshi: "complete_satoshi",
  library: "library",
  mempool: "mempool",
  authors: "authors",
  podcasts: "podcasts",
} as const satisfies Record<Category, string>;

const EXAMPLE_QUERIES = ["bitcoin", "proof of work", "double spending"];

const FLAT_PAGE_SIZE = 20;

const generateHref = (l: Locale) => urls(l).search();

function isCategory(value: string | undefined): value is Category {
  return CATEGORIES.includes(value as Category);
}

function resolveTab(tab: string | undefined): "all" | Category {
  return isCategory(tab) ? tab : "all";
}

function parsePage(page: string | undefined): number {
  const n = Number(page);
  return Number.isFinite(n) && n > 1 ? Math.floor(n) : 1;
}

export async function generateMetadata(props: LocaleParams): Promise<Metadata> {
  const params = await props.params;

  const { locale } = params;

  const { t } = await i18nTranslation(locale);
  const languages = generateHrefLangs(locales, generateHref);

  return {
    title: t("search_placeholder"),
    alternates: {
      canonical: generateHref(locale),
      languages,
    },
  };
}

type SearchPageProps = LocaleParams<
  object,
  { searchParams: Promise<{ q?: string; tab?: string; page?: string }> }
>;

export default async function SearchPage(props: SearchPageProps) {
  const params = await props.params;
  const searchParams = await props.searchParams;

  const { locale } = params;

  const { t } = await i18nTranslation(locale);

  const q = (searchParams.q ?? "").trim();
  const tab = resolveTab(searchParams.tab);
  const page = parsePage(searchParams.page);

  return (
    <PageLayout t={t} locale={locale} generateHref={generateHref} size="lg">
      <PageHeader title={t("search_placeholder")} />
      {q ? (
        tab === "all" ? (
          <GroupedResults t={t} locale={locale} q={q} />
        ) : (
          <FlatResults t={t} locale={locale} q={q} tab={tab} page={page} />
        )
      ) : (
        <EmptyPrompt locale={locale} />
      )}
    </PageLayout>
  );
}

type TabBarProps = {
  t: TFunction<"common">;
  locale: Locale;
  q: string;
  active: "all" | Category;
  counts: CountsByCategory;
};

function TabBar({ t, locale, q, active, counts }: TabBarProps) {
  const nf = new Intl.NumberFormat(locale);
  const total = CATEGORIES.reduce((sum, c) => sum + (counts[c] ?? 0), 0);

  const tabs: { key: "all" | Category; label: string; count: number }[] = [
    { key: "all", label: t("all"), count: total },
    ...CATEGORIES.map((c) => ({
      key: c,
      label: t(CATEGORY_LABEL_KEYS[c]),
      count: counts[c] ?? 0,
    })),
  ];

  return (
    <nav className="border-taupe-light mb-6 flex flex-wrap gap-x-4 gap-y-2 border-b border-dashed pb-3">
      {tabs.map(({ key, label, count }) => {
        const isActive = key === active;
        return (
          <Link
            key={key}
            href={urls(locale).search({
              q,
              tab: key === "all" ? undefined : key,
            })}
            aria-current={isActive ? "page" : undefined}
            className={clsx(
              "small-caps text-sm",
              isActive
                ? "text-cardinal font-bold"
                : "text-dark/70 hover:text-cardinal",
            )}
          >
            {label}{" "}
            <span className="text-dark/50 tabular-nums">
              {nf.format(count)}
            </span>
          </Link>
        );
      })}
    </nav>
  );
}

type ResultRowProps = {
  t: TFunction<"common">;
  locale: Locale;
  item: SearchResult;
};

function ResultRow({ t, locale, item }: ResultRowProps) {
  const date = item.date ? new Date(item.date) : null;

  return (
    <article className="border-taupe-light border-t border-dashed py-4 first:border-t-0">
      <h3 className="font-bold md:text-lg">
        <Link
          className="text-cardinal hover:underline"
          href={searchResultHref(locale, item)}
        >
          {item.title}
        </Link>
      </h3>
      <p className="mt-1">
        <SearchHighlight snippet={item.snippet} />
      </p>
      <p className="small-caps text-dark/60 mt-1 text-xs">
        <span>{t(CATEGORY_LABEL_KEYS[item.category as Category])}</span>
        {date ? (
          <>
            <span className="mx-1">•</span>
            <time dateTime={date.toISOString()}>
              {formatDate(locale, date, { dateStyle: "medium" })}
            </time>
          </>
        ) : null}
      </p>
    </article>
  );
}

type GroupedResultsProps = {
  t: TFunction<"common">;
  locale: Locale;
  q: string;
};

async function GroupedResults({ t, locale, q }: GroupedResultsProps) {
  const { data } = await api.search.search({
    query: { q, locale },
  });

  if (!data) {
    return <NoResults t={t} q={q} />;
  }

  const counts = data.countsByCategory;
  const grouped = CATEGORIES.map((category) => ({
    category,
    count: counts[category] ?? 0,
    items: data.results.filter((r) => r.category === category),
  })).filter((group) => group.items.length > 0);

  return (
    <>
      <TabBar t={t} locale={locale} q={q} active="all" counts={counts} />
      {grouped.length > 0 ? (
        <div className="flex flex-col gap-y-8">
          {grouped.map(({ category, count, items }) => (
            <section key={category}>
              <h2 className="small-caps mb-2 text-lg font-semibold">
                {t(CATEGORY_LABEL_KEYS[category])}
              </h2>
              <div>
                {items.map((item, i) => (
                  <ResultRow
                    key={`${item.entityType}-${i}`}
                    t={t}
                    locale={locale}
                    item={item}
                  />
                ))}
              </div>
              {count > items.length ? (
                <p className="mt-3">
                  <Link
                    className="text-cardinal small-caps text-sm hover:underline"
                    href={urls(locale).search({ q, tab: category })}
                  >
                    {t("search_see_all")} (
                    {t("search_results_count", { count })})
                  </Link>
                </p>
              ) : null}
            </section>
          ))}
        </div>
      ) : (
        <NoResults t={t} q={q} />
      )}
    </>
  );
}

type FlatResultsProps = {
  t: TFunction<"common">;
  locale: Locale;
  q: string;
  tab: Category;
  page: number;
};

async function FlatResults({ t, locale, q, tab, page }: FlatResultsProps) {
  const { data } = await api.search.search({
    query: { q, locale, category: tab, page },
  });

  if (!data) {
    return <NoResults t={t} q={q} />;
  }

  const counts = data.countsByCategory;
  const total = data.total;
  const hasPrev = page > 1;
  const hasNext = page * FLAT_PAGE_SIZE < total;

  return (
    <>
      <TabBar t={t} locale={locale} q={q} active={tab} counts={counts} />
      {data.results.length > 0 ? (
        <>
          <p className="small-caps text-dark/60 mb-2 text-sm">
            {t("search_results_count", { count: total })}
          </p>
          <div>
            {data.results.map((item, i) => (
              <ResultRow
                key={`${item.entityType}-${i}`}
                t={t}
                locale={locale}
                item={item}
              />
            ))}
          </div>
          {hasPrev || hasNext ? (
            <nav className="mt-6 flex justify-between">
              {hasPrev ? (
                <Link
                  className="text-cardinal small-caps text-sm hover:underline"
                  href={urls(locale).search({ q, tab, page: page - 1 })}
                >
                  &larr; Previous
                </Link>
              ) : (
                <span />
              )}
              {hasNext ? (
                <Link
                  className="text-cardinal small-caps text-sm hover:underline"
                  href={urls(locale).search({ q, tab, page: page + 1 })}
                >
                  Next &rarr;
                </Link>
              ) : (
                <span />
              )}
            </nav>
          ) : null}
        </>
      ) : (
        <NoResults t={t} q={q} />
      )}
    </>
  );
}

function NoResults({ t, q }: { t: TFunction<"common">; q: string }) {
  return (
    <div className="py-8">
      <p className="text-lg">{t("search_no_results", { query: q })}</p>
      <p className="text-dark/70 mt-2">
        Try broadening your search or using fewer, more general terms.
      </p>
    </div>
  );
}

function EmptyPrompt({ locale }: { locale: Locale }) {
  return (
    <div className="py-8">
      <p className="text-lg">Explore the archives. Try:</p>
      <ul className="mt-3 flex flex-wrap gap-2">
        {EXAMPLE_QUERIES.map((example) => (
          <li key={example}>
            <Link
              className="border-taupe-light text-cardinal small-caps inline-block rounded-full border border-dashed px-3 py-1 text-sm hover:underline"
              href={urls(locale).search({ q: example })}
            >
              {example}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
