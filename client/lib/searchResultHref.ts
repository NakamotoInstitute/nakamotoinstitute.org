import type { EmailSource, ForumPostSource, SearchResult } from "@/lib/api";
import { urls } from "@/lib/urls";

/**
 * Build the destination href for a search result, switching on `entity_type`.
 *
 * All links are built through `urls(locale)` so the satoshi.* subdomain mapping
 * and locale prefix stay correct (S3). For locale-scoped entities (library /
 * mempool / authors) the link is built from the row's own indexed locale
 * (`ref.locale`) so it always resolves to a build-time-guaranteed page; for
 * English-only entities the current UI `locale` is used.
 *
 * `item.ref` is typed loosely (`Record<string, unknown>`) by the generated SDK,
 * so each field is read with an explicit cast to the type its URL builder needs.
 */
export function searchResultHref(locale: Locale, item: SearchResult): string {
  const u = urls(locale);
  const r = item.ref as Record<string, unknown>;

  switch (item.entityType) {
    case "forum_post":
      return u.satoshi.posts.sourcePost(
        r.source as ForumPostSource,
        String(r.satoshiId),
      );
    case "email":
      return u.satoshi.emails.sourceEmail(
        r.source as EmailSource,
        String(r.satoshiId),
      );
    case "quote":
      if (r.sourceType === "whitepaper") return u.library.doc("bitcoin");
      if (r.sourceType === "post")
        return u.satoshi.posts.sourcePost(
          r.postSource as ForumPostSource,
          String(r.postSatoshiId),
        );
      return u.satoshi.emails.sourceEmail(
        r.emailSource as EmailSource,
        String(r.emailSatoshiId),
      );
    case "skeptic":
      return `${u.skeptics}#${String(r.slug)}`;
    case "library_doc":
      return urls(r.locale as Locale).library.doc(r.slug as string);
    case "library_node":
      return urls(r.locale as Locale).library.docNode(
        r.docSlug as string,
        r.nodeSlug as string,
      );
    case "mempool_post":
      return urls(r.locale as Locale).mempool.post(r.slug as string);
    case "mempool_series":
      return urls(r.locale as Locale).mempool.seriesDetail(r.slug as string);
    case "author":
      return urls(r.locale as Locale).authors.detail(r.slug as string);
    case "podcast":
      return u.podcasts.show(r.slug as string);
    case "episode":
      return u.podcasts.episode(
        r.podcastSlug as string,
        r.episodeSlug as string,
      );
    default:
      return u.search();
  }
}
