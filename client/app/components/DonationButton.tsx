"use client";

import {
  DonationLinkLocation,
  trackDonationPaymentLink,
} from "@/app/utils/analytics";
import { externalUrls } from "@/lib/urls-client";

import { ButtonLink, ButtonLinkProps } from "./Button";

type DonationButtonProps = Omit<ButtonLinkProps, "href"> & {
  trackingLocation: DonationLinkLocation;
};

export function DonationButton({
  trackingLocation,
  children,
  ...props
}: DonationButtonProps) {
  return (
    <ButtonLink
      {...props}
      href={externalUrls.zaprite}
      onClick={() => trackDonationPaymentLink(trackingLocation)}
    >
      {children}
    </ButtonLink>
  );
}
