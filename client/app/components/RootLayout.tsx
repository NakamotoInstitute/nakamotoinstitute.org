import clsx from "clsx";
import { IBM_Plex_Mono, STIX_Two_Text } from "next/font/google";
import "../globals.css";

const stix = STIX_Two_Text({
  subsets: ["latin"],
  variable: "--font-stix",
});

const plexMono = IBM_Plex_Mono({
  subsets: ["latin"],
  variable: "--font-ibm-plex-mono",
  weight: ["400", "500"],
});

export function RootLayout({
  locale,
  children,
}: {
  locale: Locale;
  children: React.ReactNode;
}) {
  return (
    <html
      lang={locale}
      className={clsx(
        stix.variable,
        plexMono.variable,
        "bg-bone text-night font-serif",
      )}
    >
      {children}
    </html>
  );
}