import clsx from "clsx";
import Big from "big.js";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { commafy } from "@/utils/strings";
import { DCAData } from "@/utils/prices";

const DAILY_BUY = new Big(1);

type PriceDatumProps = {
  label: string;
  amount: Big;
  type?: "usd" | "btc" | "perc";
  unit?: boolean;
  colored?: boolean;
};

function PriceDatum({
  label,
  amount,
  type = "usd",
  unit = true,
  colored = false,
}: PriceDatumProps) {
  const precision = type === "btc" ? 8 : 2;
  let formattedAmount = commafy(amount.toFixed(precision));

  // Add units if necessary
  if (unit) {
    switch (type) {
      case "usd":
        formattedAmount = `$${formattedAmount}`;
        break;
      case "btc":
        formattedAmount = `${formattedAmount} BTC`;
        break;
      case "perc":
        formattedAmount = `${formattedAmount}%`;
        break;
    }
  }

  return (
    <div className="flex flex-row whitespace-nowrap md:flex-col md:text-center">
      <div className="basis-1/2 font-bold">{label}</div>
      <div
        className={clsx(
          "basis-1/2",
          colored && {
            "text-green-600": amount.gt(0),
            "text-red-600": amount.lt(0),
          },
        )}
      >
        {formattedAmount}
      </div>
    </div>
  );
}

type SkepticPriceDataProps = {
  locale: Locale;
  priceData: DCAData;
};

export async function SkepticPriceData({
  locale,
  priceData: { usdInvested, totalBtc, usdValue, change },
}: SkepticPriceDataProps) {
  const { t } = await i18nTranslation(locale);
  return (
    <div className="flex flex-col flex-wrap justify-between border-b border-t border-night border-opacity-25 py-2 md:flex-row">
      <PriceDatum label={t("Daily buy")} amount={Big(DAILY_BUY)} />
      <PriceDatum label={t("Total invested")} amount={usdInvested} />
      <PriceDatum
        label={t("BTC balance")}
        amount={totalBtc}
        type="btc"
        unit={false}
      />
      <PriceDatum label={t("Current value")} amount={usdValue} />
      <PriceDatum
        label={t("Percent change")}
        amount={change}
        type="perc"
        colored
      />
    </div>
  );
}
