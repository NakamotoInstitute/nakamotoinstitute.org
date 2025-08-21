import { getMempoolFeed } from "@/lib/api/mempool";

export const dynamic = "force-static";

export async function GET(
  _request: Request,
  ctx: RouteContext<"/[locale]/mempool/atom.xml">,
) {
  const { locale } = await ctx.params;
  const content = await getMempoolFeed(locale as Locale, "atom");

  return new Response(content, {
    headers: {
      "Content-Type": "application/atom+xml",
      "Content-Disposition": 'attachment; filename="atom.xml"',
    },
  });
}
