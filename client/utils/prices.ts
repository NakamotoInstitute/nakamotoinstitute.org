import Big from "big.js";
import { Price } from "@/lib/api";
import { calculateDayDifference } from "@/utils/dates";

const DAILY_BUY = new Big(1);

export function calculateDCA(date: Date, prices: Price[], dailyBuy: Big) {
  const idx = prices.findIndex(
    (item) => item.date.getTime() === date.getTime(),
  );
  const dcaPrices = prices.slice(idx);
  const [first, ...rest] = dcaPrices;
  const last = rest[rest.length - 1];
  const dayDiff = calculateDayDifference(first.date, last.date);
  const usdInvested = Big(dayDiff).times(dailyBuy).plus(dailyBuy);
  const totalBtc = dcaPrices
    .map((d) => d.price)
    .reduce((val, curr) => {
      const amount = Big(1).div(curr).round(8);
      return val.add(amount);
    }, Big(0));
  const usdValue = totalBtc.times(last.price).round(2);
  const change = usdValue
    .minus(usdInvested)
    .div(usdInvested)
    .times(100)
    .round(2);
  return {
    originalUsd: first.price,
    usdInvested,
    totalBtc,
    usdValue,
    change,
  };
}

export type DCAData = ReturnType<typeof calculateDCA>;
