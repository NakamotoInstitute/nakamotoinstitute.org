import Big from "big.js";
import clsx from "clsx";
import { TFunction } from "i18next";

import { DCAData } from "@/utils/prices";

const DAILY_BUY = new Big(1);

// USD is always formatted as en-US (historical price data)
const USD_FORMATTER = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
});

const getBtcFormatter = (locale: Locale) =>
  new Intl.NumberFormat(locale, {
    minimumFractionDigits: 8,
    maximumFractionDigits: 8,
  });

const getPercentFormatter = (locale: Locale) =>
  new Intl.NumberFormat(locale, {
    style: "percent",
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });

export type Format = "usd" | "btc" | "percent";

export function formatAmount(
  amount: number,
  format: Format,
  locale: Locale,
): string {
  switch (format) {
    case "usd":
      return USD_FORMATTER.format(amount);
    case "btc":
      return getBtcFormatter(locale).format(amount);
    case "percent":
      return getPercentFormatter(locale).format(amount / 100);
  }
}

type PriceDatumProps = {
  label: string;
  amount: Big;
  format: Format;
  locale: Locale;
  colored?: boolean;
};

function PriceDatum({
  label,
  amount,
  format,
  locale,
  colored = false,
}: PriceDatumProps) {
  const formattedAmount = formatAmount(amount.toNumber(), format, locale);

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
  t: TFunction<string, string>;
  locale: Locale;
  priceData: DCAData;
};

export function SkepticPriceData({
  t,
  locale,
  priceData: { usdInvested, totalBtc, usdValue, change },
}: SkepticPriceDataProps) {
  return (
    <div className="border-taupe-light flex flex-col flex-wrap justify-between border-y border-dashed py-2 md:flex-row">
      <PriceDatum
        label={t("daily_buy")}
        amount={Big(DAILY_BUY)}
        format="usd"
        locale={locale}
      />
      <PriceDatum
        label={t("total_invested")}
        amount={usdInvested}
        format="usd"
        locale={locale}
      />
      <PriceDatum
        label={t("btc_balance")}
        amount={totalBtc}
        format="btc"
        locale={locale}
      />
      <PriceDatum
        label={t("current_value")}
        amount={usdValue}
        format="usd"
        locale={locale}
      />
      <PriceDatum
        label={t("percent_change")}
        amount={change}
        format="percent"
        locale={locale}
        colored
      />
    </div>
  );
}
