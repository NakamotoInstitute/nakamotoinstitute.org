import Link from "next/link";
import Big from "big.js";
import { Markdown } from "@/app/components";
import { Price, Skeptic } from "@/lib/api";
import { i18nTranslation } from "@/lib/i18n";
import { commafy } from "@/utils/strings";
import { formatDate } from "@/utils/dates";
import { calculateDCA } from "@/utils/prices";
import { SkepticPriceData } from "./PriceData";

const DAILY_BUY = new Big(1);

export async function Skeptic({
  locale,
  skeptic,
  prices,
}: {
  locale: Locale;
  skeptic: Skeptic;
  prices: Price[];
}) {
  const { t } = await i18nTranslation(locale);
  const priceData = calculateDCA(skeptic.date, prices, DAILY_BUY);

  return (
    <article
      id={skeptic.slug}
      className="border-b border-solid border-night py-4 first:pt-0 last:border-b-0"
    >
      <header>
        <p className="text-2xl">
          {formatDate(locale, skeptic.date)} • $
          {commafy(priceData.originalUsd.toFixed(2))}
        </p>
        <h2 className="text-3xl">{skeptic.name}</h2>
        <p className="italic">{skeptic.title}</p>
      </header>
      <section className="py-2">
        <SkepticPriceData locale={locale} priceData={priceData} />
      </section>
      <section>
        {skeptic.excerpt ? <Markdown>{skeptic.excerpt}</Markdown> : null}
        {skeptic.waybackLink ? (
          <p>
            <Link href={skeptic.waybackLink}>{t("Archive link")}</Link>
          </p>
        ) : null}
      </section>
    </article>
  );
}