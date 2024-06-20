"use client";

import clsx from "clsx";
import Link from "next/link";
import { useState } from "react";

import { languages } from "@/i18n";

import { LanguageToggle, ToggleLinkProps } from "./LanguageToggle";

export function Navbar({
  locale,
  logo,
  homeHref,
  navLinks,
  ...toggleProps
}: ToggleLinkProps & {
  locale: Locale;
  logo: React.ReactNode;
  homeHref: string;
  navLinks: AnchorProps[];
}) {
  const [menuOpen, setMenuOpen] = useState(false);
  const current = languages[locale];

  return (
    <nav className="mb-4 border-b border-dashed border-dark">
      <div className="twbs-container font-bold">
        <div className="relative flex items-center justify-between py-6">
          <div className="absolute inset-y-0 left-0 flex items-center md:hidden">
            <button
              id="mobileMenuButton"
              type="button"
              className="inline-flex items-center justify-center rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-inset"
              aria-controls="mobile-menu"
              aria-expanded={menuOpen}
              onClick={() => setMenuOpen(!menuOpen)}
            >
              <span className="sr-only">Open main menu</span>
              <svg
                id="mobileMenuIconClosed"
                className={clsx("h-6 w-6", { hidden: menuOpen })}
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                aria-hidden={menuOpen}
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M4 6h16M4 12h16M4 18h16"
                />
              </svg>
              <svg
                id="mobileMenuIconOpen"
                className={clsx("h-6 w-6", { hidden: !menuOpen })}
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                aria-hidden={!menuOpen}
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>
          <div className="flex flex-1 items-center justify-center md:items-stretch md:justify-start">
            <div className="flex flex-shrink-0 items-center">
              <Link href={homeHref}>{logo}</Link>
            </div>
            <div className="hidden h-12 items-center md:ml-auto md:flex md:space-x-4">
              {navLinks.map(({ href, text }) => (
                <Link key={text} href={href} className="p-2 text-dark">
                  {text}
                </Link>
              ))}
            </div>
          </div>
          <div className="absolute inset-y-0 right-0 flex items-center pr-2 md:static md:inset-auto md:ml-6 md:pr-0">
            <LanguageToggle current={current} {...toggleProps} />
          </div>
        </div>
      </div>
      <div className={clsx("md:hidden", { hidden: !menuOpen })} id="mobileMenu">
        <div className="space-y-1 px-2 pb-3 pt-2">
          {navLinks.map(({ href, text }) => (
            <Link key={text} href={href} className="block px-3 py-2 text-dark">
              {text}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  );
}
