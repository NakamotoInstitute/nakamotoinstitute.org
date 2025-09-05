import { trackEvent } from "fathom-client";

export type DonationLinkLocation = "nav" | "footer" | "home" | "page";

export function trackDonationPaymentLink(location: DonationLinkLocation) {
  trackEvent(`donate_payment_link:${location}`);
}
