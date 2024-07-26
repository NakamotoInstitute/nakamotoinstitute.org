import Big from "big.js";
import clsx from "clsx";
import { TFunction } from "i18next";

import { DCAData } from "@/utils/prices";
import { commafy } from "@/utils/strings";

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
  t: TFunction<string, string>;
  priceData: DCAData;
};

export async function SkepticPriceData({
  t,
  priceData: { usdInvested, totalBtc, usdValue, change },
}: SkepticPriceDataProps) {
  return (
    <div className="flex flex-col flex-wrap justify-between border-y border-dashed border-taupe-light py-2 md:flex-row">
      <PriceDatum label={t("daily_buy")} amount={Big(DAILY_BUY)} />
      <PriceDatum label={t("total_invested")} amount={usdInvested} />
      <PriceDatum
        label={t("btc_balance")}
        amount={totalBtc}
        type="btc"
        unit={false}
      />
      <PriceDatum label={t("current_value")} amount={usdValue} />
      <PriceDatum
        label={t("percent_change")}
        amount={change}
        type="perc"
        colored
      />
    </div>
  );
}
