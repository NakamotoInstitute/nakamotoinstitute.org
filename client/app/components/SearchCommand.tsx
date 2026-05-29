"use client";

import * as Dialog from "@radix-ui/react-dialog";
import clsx from "clsx";
import { Command } from "cmdk";
import { useRouter } from "next/navigation";
import { useCallback, useEffect, useRef, useState } from "react";

import { SearchHighlight } from "@/app/components/SearchHighlight";
import type { CountsByCategory, SearchResponse, SearchResult } from "@/lib/api";
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
  "authors",
  "podcasts",
];

// A17: zero-query example pills.
const EXAMPLE_QUERIES = ["Proof of Work", "Hal Finney", "Block Size"];

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

function SearchIcon({ className }: { className?: string }) {
  return (
    <svg
      className={className}
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
        d="m21 21-4.35-4.35M11 18a7 7 0 1 0 0-14 7 7 0 0 0 0 14Z"
      />
    </svg>
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
  const [loading, setLoading] = useState(false);

  const triggerRef = useRef<HTMLAnchorElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const abortRef = useRef<AbortController | null>(null);
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Close + reset all transient state. Routed through every close path (Esc,
  // overlay click, ⌘K toggle, navigation) so resetting happens in an event
  // handler, never synchronously inside an effect.
  const closePalette = useCallback(() => {
    setOpen(false);
    setQuery("");
    setResults([]);
    setLoading(false);
    abortRef.current?.abort();
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
        setLoading(false);
        return;
      }

      setLoading(true);
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
          setLoading(false);
        })
        .catch((error: unknown) => {
          if (error instanceof DOMException && error.name === "AbortError") {
            return;
          }
          setResults([]);
          setLoading(false);
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
    const separator = searchHref.includes("?") ? "&" : "?";
    closeAndGo(`${searchHref}${separator}q=${encodeURIComponent(trimmed)}`);
  }, [query, searchHref, closeAndGo]);

  // Group results by category, preserving rank order within each bucket.
  const grouped = CATEGORY_ORDER.map((category) => ({
    category,
    items: results.filter((item) => item.category === category),
  })).filter((group) => group.items.length > 0);

  const hasQuery = query.trim().length > 0;
  const showNoResults = hasQuery && !loading && results.length === 0;

  return (
    <>
      {/* Progressive enhancement: a real anchor to /search that the palette
          intercepts when JS is active. Desktop = fake input + ⌘K hint;
          collapses to an icon below md. */}
      <Dialog.Root
        open={open}
        onOpenChange={(next) => (next ? setOpen(true) : closePalette())}
      >
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
          className="text-taupe hover:text-dark flex items-center transition-colors focus:outline-hidden"
        >
          {/* Mobile (< md): icon only */}
          <span className="flex items-center p-2 md:hidden">
            <SearchIcon className="h-5 w-5" />
            <span className="sr-only">{labels.search}</span>
          </span>
          {/* Desktop (>= md): fake input with ⌘K hint */}
          <span className="border-sand hover:border-dark hidden h-9 w-56 items-center gap-x-2 rounded-xs border px-3 text-sm font-normal transition-colors md:flex">
            <SearchIcon className="h-4 w-4 shrink-0" />
            <span className="text-taupe truncate text-start">
              {labels.placeholder}
            </span>
            <kbd className="border-sand text-taupe ms-auto rounded-xs border px-1.5 py-0.5 font-mono text-xs">
              ⌘K
            </kbd>
          </span>
        </a>

        <Dialog.Portal>
          <Dialog.Overlay className="bg-dark/40 fixed inset-0 z-50 motion-safe:transition-opacity motion-safe:duration-150 motion-safe:data-[state=closed]:opacity-0" />
          <Dialog.Content
            dir={dir}
            aria-label={labels.search}
            className={clsx(
              "fixed z-50 flex flex-col bg-white shadow-lg focus:outline-hidden",
              // Mobile: full-screen sheet with safe-area padding.
              "inset-0 h-[100dvh] w-full pt-[env(safe-area-inset-top)] pb-[env(safe-area-inset-bottom)]",
              // Desktop: centered panel.
              "md:inset-auto md:start-1/2 md:top-24 md:h-auto md:max-h-[70vh] md:w-full md:max-w-xl md:-translate-x-1/2 md:rounded-md md:pt-0 md:pb-0 rtl:md:translate-x-1/2",
              "motion-safe:transition motion-safe:duration-150 motion-safe:data-[state=closed]:opacity-0",
            )}
            onCloseAutoFocus={(event) => {
              // Esc/close restores focus to the trigger.
              event.preventDefault();
              triggerRef.current?.focus();
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
                // Enter with no item focused -> navigate to the /search page.
                if (event.key === "Enter" && !event.defaultPrevented) {
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
                <SearchIcon className="text-taupe h-5 w-5 shrink-0" />
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
                    className="text-taupe hover:text-dark flex shrink-0 cursor-pointer items-center transition-colors"
                  >
                    <svg
                      className="h-5 w-5"
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
                        d="M6 18 18 6M6 6l12 12"
                      />
                    </svg>
                  </button>
                ) : null}
              </div>

              <div aria-live="polite" className="sr-only">
                {loading
                  ? labels.placeholder
                  : showNoResults
                    ? labels.noResults.replace("{{query}}", query.trim())
                    : ""}
              </div>

              <Command.List className="min-h-0 flex-1 overflow-y-auto overscroll-contain p-2">
                {!hasQuery ? (
                  <div className="px-2 py-3">
                    <p className="text-taupe text-sm">{labels.placeholder}</p>
                    <div className="mt-3 flex flex-wrap gap-2">
                      {EXAMPLE_QUERIES.map((example) => (
                        <button
                          key={example}
                          type="button"
                          onClick={() => {
                            setQuery(example);
                            inputRef.current?.focus();
                          }}
                          className="border-sand text-dark hover:border-dark hover:text-cardinal cursor-pointer rounded-full border px-3 py-1 text-sm transition-colors"
                        >
                          {example}
                        </button>
                      ))}
                    </div>
                  </div>
                ) : null}

                {showNoResults ? (
                  <Command.Empty className="px-2 py-6 text-sm">
                    <p className="text-dark">
                      {labels.noResults.replace("{{query}}", query.trim())}
                    </p>
                    <p className="text-taupe mt-1">
                      Try checking your spelling or using broader terms.
                    </p>
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
                  className="border-sand text-dark hover:bg-cream flex w-full shrink-0 cursor-pointer items-center justify-between border-t px-4 py-3 text-sm font-bold transition-colors"
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
