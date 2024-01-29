import { getMempoolFeed } from "@/lib/api/mempool";

export async function GET(
  _request: Request,
  { params: { locale } }: LocaleParams,
) {
  const content = await getMempoolFeed(locale, "atom");

  return new Response(content, {
    headers: {
      "Content-Type": "application/atom+xml",
      "Content-Disposition": 'attachment; filename="atom.xml"',
    },
  });
}
