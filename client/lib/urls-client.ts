// Client-safe URL utilities that don't depend on server-side environment variables

export const externalUrls = {
  github: "https://github.com/NakamotoInstitute/nakamotoinstitute.org",
  nostr: "https://primal.net/sni",
  rumble: {
    channel: "https://rumble.com/c/SatoshiNakamotoInstitute",
    link: (id: string) => `https://rumble.com/${id}.html`,
  },
  substack: "https://news.nakamotoinstitute.org",
  x: "https://x.com/NakamotoInst",
  youtube: {
    channel: "https://www.youtube.com/@SatoshiNakamotoInstitute",
    embed: (id: string) => `https://www.youtube.com/embed/${id}?rel=0`,
  },
  zaprite: "https://pay.zaprite.com/pl_vNYDp4YBSd",
};