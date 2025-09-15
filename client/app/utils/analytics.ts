import { trackEvent } from "fathom-client";

export type DonationLinkLocation = "nav" | "footer" | "home" | "page";

const DONATION_COOLDOWN_MS = 5000; // 5 seconds

function trackEventOnce(eventName: string, cooldownMs = 5000) {
  if (typeof window === "undefined") {
    return; // SSR safety
  }

  const key = `fathom:${eventName}`;
  const now = Date.now();

  try {
    const last = sessionStorage.getItem(key);
    if (last && now - parseInt(last, 10) < cooldownMs) {
      return; // Within cooldown
    }

    sessionStorage.setItem(key, String(now));
  } catch {
    // SessionStorage unavailable (private browsing, etc)
    // Track anyway - better to over-track than miss events
  }

  trackEvent(eventName);
}

export function trackDonationPaymentLink(location: DonationLinkLocation) {
  trackEventOnce(`donate_payment_link:${location}`, DONATION_COOLDOWN_MS);
}
