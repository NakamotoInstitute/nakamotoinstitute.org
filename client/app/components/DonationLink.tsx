"use client";

import Link from "next/link";

import {
  DonationLinkLocation,
  trackDonationPaymentLink,
} from "@/app/utils/analytics";
import { externalUrls } from "@/lib/urls-client";

type DonationLinkProps = {
  className?: string;
  children: React.ReactNode;
  trackingLocation: DonationLinkLocation;
};

export function DonationLink({
  className,
  children,
  trackingLocation,
}: DonationLinkProps) {
  return (
    <Link
      href={externalUrls.zaprite}
      className={className}
      onClick={() => trackDonationPaymentLink(trackingLocation)}
    >
      {children}
    </Link>
  );
}
