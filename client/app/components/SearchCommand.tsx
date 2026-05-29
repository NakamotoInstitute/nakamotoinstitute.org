"use client";

import * as Dialog from "@radix-ui/react-dialog";
import clsx from "clsx";
import { Command } from "cmdk";
import { usePathname, useRouter } from "next/navigation";
import { useCallback, useEffect, useRef, useState } from "react";

import { CloseIcon } from "@/app/components/CloseIcon";
import { SearchHighlight } from "@/app/components/SearchHighlight";
import { SearchIcon } from "@/app/components/SearchIcon";
import type { CountsByCategory, SearchResponse, SearchResult } from "@/lib/api";
import { focusRing, focusRingInset } from "@/lib/focusRing";
import { isRtl } from "@/i18n";

export type SearchLabels = {
  search: string;
  placeholder: string;
  noResults: string;
  seeAll: string;
  all: string;
  satoshi: string;
  library: string;
  mempool: string;
  authors: string;
  podcasts: string;
};

type CategoryKey = keyof CountsByCategory;

// The Route Handler enriches each result with a server-built href (urls() reads
// server-only env, so it cannot run in this client component).
type PaletteResult = SearchResult & { href: string };
type PaletteResponse = Omit<SearchResponse, "results"> & {
  results: PaletteResult[];
};

const CATEGORY_ORDER: CategoryKey[] = [
  "satoshi",
  "library",
  "mempool",
  "podcasts",
];

const DEBOUNCE_MS = 250;

function categoryLabel(labels: SearchLabels, category: CategoryKey): string {
  switch (category) {
    case "satoshi":
      return labels.satoshi;
    case "library":
      return labels.library;
    case "mempool":
      return labels.mempool;
    case "authors":
      return labels.authors;
    case "podcasts":
      return labels.podcasts;
    default:
      return category;
  }
}

// Shimmer placeholder shown while a query is pending, so the results area never
// flashes "no results" before the fetch settles.
function ResultsSkeleton() {
  return (
    <div className="space-y-4 px-2 py-2" aria-hidden="true">
      {[0, 1, 2, 3].map((row) => (
        <div key={row} className="space-y-1.5">
          <div className="bg-sand h-4 w-1/2 rounded-sm motion-safe:animate-pulse" />
          <div className="bg-sand/60 h-3 w-full rounded-sm motion-safe:animate-pulse" />
          <div className="bg-sand/60 h-3 w-4/5 rounded-sm motion-safe:animate-pulse" />
        </div>
      ))}
    </div>
  );
}

export function SearchCommand({
  locale,
  labels,
  searchHref,
}: {
  locale: Locale;
  labels: SearchLabels;
  searchHref: string;
}) {
  const router = useRouter();
  const dir = isRtl(locale) ? "rtl" : "ltr";

  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<PaletteResult[]>([]);
  const [counts, setCounts] = useState<CountsByCategory | null>(null);
  const [selected, setSelected] = useState<Set<CategoryKey>>(new Set());
  // The query that the currently-displayed results reflect. Set only in the
  // async fetch callbacks (never synchronously in an effect), so it doubles as
  // the "settled" signal: results are pending whenever it lags the input.
  const [resultsQuery, setResultsQuery] = useState("");

  const triggerRef = useRef<HTMLAnchorElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const abortRef = useRef<AbortController | null>(null);
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Hide the navbar trigger on the /search page itself (the page has its own
  // input box); the global ⌘K shortcut still opens the palette there. Compared
  // by pathname so it holds across locales (searchHref carries the locale).
  const pathname = usePathname();
  const searchPathname = new URL(searchHref, "http://n").pathname.replace(
    /\/+$/,
    "",
  );
  const isSearchPage = (pathname ?? "").replace(/\/+$/, "") === searchPathname;

  // Close + reset all transient state. Routed through every close path (Esc,
  // overlay click, ⌘K toggle, navigation) so resetting happens in an event
  // handler, never synchronously inside an effect.
  const closePalette = useCallback(() => {
    setOpen(false);
    setQuery("");
    setResults([]);
    setCounts(null);
    setSelected(new Set());
    setResultsQuery("");
    abortRef.current?.abort();
  }, []);

  // Toggle a category in/out of the "search in" filter (empty set = everywhere).
  const toggleCategory = useCallback((category: CategoryKey) => {
    setSelected((prev) => {
      const next = new Set(prev);
      if (next.has(category)) {
        next.delete(category);
      } else {
        next.add(category);
      }
      return next;
    });
  }, []);

  // Global ⌘K / Ctrl+K (and optional "/") to open from any page.
  useEffect(() => {
    function onKeyDown(event: KeyboardEvent) {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
        event.preventDefault();
        if (open) {
          closePalette();
        } else {
          setOpen(true);
        }
        return;
      }
      if (event.key === "/" && !open) {
        const target = event.target as HTMLElement | null;
        const tag = target?.tagName;
        if (
          tag === "INPUT" ||
          tag === "TEXTAREA" ||
          target?.isContentEditable
        ) {
          return;
        }
        event.preventDefault();
        setOpen(true);
      }
    }
    document.addEventListener("keydown", onKeyDown);
    return () => document.removeEventListener("keydown", onKeyDown);
  }, [open, closePalette]);

  // Debounced fetch from the Route Handler; AbortController cancels stale
  // requests; prior results stay visible while loading. All state updates run
  // inside the debounced callback (never synchronously in the effect body).
  useEffect(() => {
    const trimmed = query.trim();

    if (debounceRef.current) clearTimeout(debounceRef.current);

    debounceRef.current = setTimeout(() => {
      abortRef.current?.abort();

      if (trimmed.length === 0) {
        setResults([]);
        setCounts(null);
        setResultsQuery("");
        return;
      }

      const controller = new AbortController();
      abortRef.current = controller;

      const params = new URLSearchParams({ q: trimmed, locale });
      fetch(`/api/search?${params.toString()}`, {
        signal: controller.signal,
      })
        .then((res) => (res.ok ? (res.json() as Promise<PaletteResponse>) : null))
        .then((data) => {
          if (controller.signal.aborted) return;
          setResults(data?.results ?? []);
          setCounts(data?.countsByCategory ?? null);
          setResultsQuery(trimmed);
        })
        .catch((error: unknown) => {
          if (error instanceof DOMException && error.name === "AbortError") {
            return;
          }
          setResults([]);
          setCounts(null);
          setResultsQuery(trimmed);
        });
    }, DEBOUNCE_MS);

    return () => {
      if (debounceRef.current) clearTimeout(debounceRef.current);
    };
  }, [query, locale]);

  const closeAndGo = useCallback(
    (href: string) => {
      closePalette();
      router.push(href);
    },
    [router, closePalette],
  );

  const goToSearchPage = useCallback(() => {
    const trimmed = query.trim();
    if (trimmed.length === 0) return;
    const params = new URLSearchParams({ q: trimmed });
    // Carry a single selected category through to the results page's tab.
    if (selected.size === 1) params.set("tab", [...selected][0]);
    const separator = searchHref.includes("?") ? "&" : "?";
    closeAndGo(`${searchHref}${separator}${params.toString()}`);
  }, [query, selected, searchHref, closeAndGo]);

  // Group results by category (rank order preserved), limited to the selected
  // categories — an empty selection means "search everywhere".
  const grouped = CATEGORY_ORDER.filter(
    (category) => selected.size === 0 || selected.has(category),
  )
    .map((category) => ({
      category,
      items: results.filter((item) => item.category === category),
    }))
    .filter((group) => group.items.length > 0);

  const trimmedQuery = query.trim();
  const hasQuery = trimmedQuery.length > 0;
  // A query is "pending" until the on-screen results reflect it — this covers
  // both the debounce window and the in-flight fetch, so we can show a loading
  // skeleton instead of briefly flashing "no results".
  const pending = hasQuery && resultsQuery !== trimmedQuery;
  const showNoResults = hasQuery && !pending && grouped.length === 0;
  // Matches exist, but not in the categories the user filtered to.
  const filteredEverythingOut = showNoResults && results.length > 0;

  return (
    <>
      {/* Progressive enhancement: a real anchor to /search that the palette
          intercepts when JS is active. Desktop = fake input + ⌘K hint;
          collapses to an icon below md. */}
      <Dialog.Root
        open={open}
        onOpenChange={(next) => (next ? setOpen(true) : closePalette())}
      >
        {isSearchPage ? null : (
          <a
            ref={triggerRef}
            href={searchHref}
            onClick={(event) => {
              // Allow modified clicks (new tab) and middle-clicks to pass through.
              if (
                event.metaKey ||
                event.ctrlKey ||
                event.shiftKey ||
                event.altKey ||
                event.button !== 0
              ) {
                return;
              }
              event.preventDefault();
              setOpen(true);
            }}
            aria-label={labels.search}
            className={clsx(
              "text-taupe hover:text-cardinal flex items-center rounded-xs transition-colors",
              focusRing,
            )}
          >
            {/* Mobile (< md): icon only */}
            <span className="flex items-center p-2 md:hidden">
              <SearchIcon className="h-5 w-5" />
              <span className="sr-only">{labels.search}</span>
            </span>
            {/* Desktop (>= md): fake input with ⌘K hint */}
            <span className="border-sand hover:border-cardinal hidden h-10 w-56 items-center gap-x-2 rounded-xs border px-3 text-sm font-normal transition-colors md:flex">
              <SearchIcon className="h-4 w-4 shrink-0" />
              <span className="text-taupe truncate text-start">
                {labels.placeholder}
              </span>
              <kbd className="border-sand text-taupe ms-auto rounded-xs border px-1.5 py-0.5 font-mono text-xs">
                ⌘K
              </kbd>
            </span>
          </a>
        )}

        <Dialog.Portal>
          {/* Mobile: dim only below the navbar so the header stays visible;
              desktop: full-screen dim behind the centered card. */}
          <Dialog.Overlay className="bg-dark/40 fixed inset-x-0 top-24 bottom-0 z-50 md:top-0 motion-safe:transition-opacity motion-safe:duration-150 motion-safe:data-[state=closed]:opacity-0" />
          <Dialog.Content
            dir={dir}
            aria-label={labels.search}
            className={clsx(
              "fixed z-50 flex flex-col bg-white shadow-lg focus:outline-hidden",
              // Mobile: panel anchored below the navbar (keeps the header
              // visible under its dashed border), filling to the bottom.
              "inset-x-0 top-24 bottom-0 w-full pb-[env(safe-area-inset-bottom)]",
              // Desktop: centered panel.
              "md:inset-auto md:start-1/2 md:top-24 md:h-auto md:max-h-[70vh] md:w-full md:max-w-xl md:-translate-x-1/2 md:rounded-md md:pt-0 md:pb-0 rtl:md:translate-x-1/2",
              "motion-safe:transition motion-safe:duration-150 motion-safe:data-[state=closed]:opacity-0",
            )}
            onCloseAutoFocus={(event) => {
              // Esc/close restores focus to the trigger when it exists; on
              // /search the trigger is hidden, so let focus return naturally.
              if (triggerRef.current) {
                event.preventDefault();
                triggerRef.current.focus();
              }
            }}
          >
            <Dialog.Title className="sr-only">{labels.search}</Dialog.Title>
            <Dialog.Description className="sr-only">
              {labels.placeholder}
            </Dialog.Description>

            <Command
              dir={dir}
              label={labels.search}
              shouldFilter={false}
              loop
              className="flex min-h-0 flex-1 flex-col"
              onKeyDown={(event) => {
                // Only the text input submits to the results page; the filter
                // chips and icon buttons handle their own Enter/Space.
                if (event.key === "Enter" && !event.defaultPrevented) {
                  if (event.target !== inputRef.current) return;
                  const hasActive = event.currentTarget.querySelector(
                    '[cmdk-item=""][aria-selected="true"]',
                  );
                  if (!hasActive) {
                    event.preventDefault();
                    goToSearchPage();
                  }
                }
              }}
            >
              <div className="border-sand flex items-center gap-x-2 border-b px-4 py-3">
                {/* Mobile: leading back control to dismiss the full-screen
                    sheet (no overlay to tap, no Esc key on touch keyboards). */}
                <button
                  type="button"
                  onClick={closePalette}
                  aria-label="Close search"
                  className={clsx(
                    "text-taupe hover:text-dark -ms-1 flex shrink-0 cursor-pointer items-center rounded-xs transition-colors md:hidden",
                    focusRing,
                  )}
                >
                  <svg
                    className="h-6 w-6 rtl:rotate-180"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth={2}
                    aria-hidden="true"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M15 19.5 7.5 12l7.5-7.5"
                    />
                  </svg>
                </button>
                <SearchIcon className="text-taupe hidden h-5 w-5 shrink-0 md:block" />
                <Command.Input
                  ref={inputRef}
                  value={query}
                  onValueChange={setQuery}
                  placeholder={labels.placeholder}
                  // text-base (>=16px) prevents iOS Safari auto-zoom on focus.
                  className="text-dark placeholder:text-taupe w-full bg-transparent text-base outline-hidden"
                  autoFocus
                />
                {query.length > 0 ? (
                  <button
                    type="button"
                    onClick={() => {
                      setQuery("");
                      inputRef.current?.focus();
                    }}
                    aria-label="Clear search"
                    className={clsx(
                      "text-taupe hover:text-dark -me-1 flex shrink-0 cursor-pointer items-center rounded-xs transition-colors",
                      focusRing,
                    )}
                  >
                    <CloseIcon className="h-6 w-6" />
                  </button>
                ) : null}
              </div>

              {/* Category filter — choose where to search (multi-select).
                  An empty selection searches everywhere; counts appear once a
                  query is entered. */}
              <div className="border-sand flex flex-wrap items-center gap-2 border-b px-4 py-2.5">
                {CATEGORY_ORDER.map((category) => {
                  const isSelected = selected.has(category);
                  const count = counts?.[category];
                  return (
                    <button
                      key={category}
                      type="button"
                      role="checkbox"
                      aria-checked={isSelected}
                      onClick={() => toggleCategory(category)}
                      className={clsx(
                        "flex cursor-pointer items-center gap-x-1.5 rounded-full border px-3 py-1 text-sm transition-colors",
                        focusRing,
                        isSelected
                          ? "border-cardinal bg-cardinal text-white"
                          : "border-sand text-dark hover:border-dark",
                      )}
                    >
                      <span>{categoryLabel(labels, category)}</span>
                      {hasQuery && count !== undefined ? (
                        <span
                          className={clsx(
                            "text-xs tabular-nums motion-safe:animate-count-in",
                            isSelected ? "text-white/80" : "text-taupe",
                          )}
                        >
                          {new Intl.NumberFormat(locale).format(count)}
                        </span>
                      ) : null}
                    </button>
                  );
                })}
              </div>

              <div aria-live="polite" className="sr-only">
                {showNoResults
                  ? labels.noResults.replace("{{query}}", query.trim())
                  : ""}
              </div>

              <Command.List
                aria-busy={pending}
                className="min-h-0 flex-1 overflow-y-auto overscroll-contain p-2"
              >
                {!hasQuery ? (
                  <p className="text-taupe px-2 py-8 text-center text-sm">
                    Don&rsquo;t trust. Verify.
                  </p>
                ) : null}

                {pending && grouped.length === 0 ? <ResultsSkeleton /> : null}

                {showNoResults ? (
                  <Command.Empty className="px-2 py-8 text-center text-sm">
                    {filteredEverythingOut ? (
                      <p className="text-dark">
                        {selected.size === 1
                          ? "No results in the selected category."
                          : "No results in the selected categories."}
                      </p>
                    ) : (
                      <>
                        <p className="text-dark">
                          {labels.noResults.replace("{{query}}", query.trim())}
                        </p>
                        <p className="text-taupe mt-1">
                          Try checking your spelling or using broader terms.
                        </p>
                      </>
                    )}
                  </Command.Empty>
                ) : null}

                {grouped.map((group) => (
                  <Command.Group
                    key={group.category}
                    heading={categoryLabel(labels, group.category)}
                    className="[&_[cmdk-group-heading]]:text-taupe [&_[cmdk-group-heading]]:px-2 [&_[cmdk-group-heading]]:py-1.5 [&_[cmdk-group-heading]]:text-xs [&_[cmdk-group-heading]]:font-bold [&_[cmdk-group-heading]]:uppercase"
                  >
                    {group.items.map((item, index) => {
                      const href = item.href;
                      return (
                        <Command.Item
                          key={`${group.category}-${index}-${item.title}`}
                          value={`${group.category}-${index}-${item.title}`}
                          onSelect={() => closeAndGo(href)}
                          className="text-dark data-[selected=true]:bg-cream flex cursor-pointer flex-col gap-y-0.5 rounded-xs px-2 py-2 text-start"
                        >
                          <span className="font-bold">{item.title}</span>
                          <span className="text-taupe line-clamp-2 text-sm">
                            <SearchHighlight snippet={item.snippet} />
                          </span>
                        </Command.Item>
                      );
                    })}
                  </Command.Group>
                ))}
              </Command.List>

              {hasQuery ? (
                <button
                  type="button"
                  onClick={goToSearchPage}
                  className={clsx(
                    "border-sand text-dark hover:bg-cream flex w-full shrink-0 cursor-pointer items-center justify-between border-t px-4 py-3 text-sm font-bold transition-colors",
                    focusRingInset,
                  )}
                >
                  <span>{labels.seeAll}</span>
                  <kbd className="border-sand text-taupe rounded-xs border px-1.5 py-0.5 font-mono text-xs">
                    ↵
                  </kbd>
                </button>
              ) : null}
            </Command>
          </Dialog.Content>
        </Dialog.Portal>
      </Dialog.Root>
    </>
  );
}
