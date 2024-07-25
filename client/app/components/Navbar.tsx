"use client";

import clsx from "clsx";
import Link from "next/link";
import { useState } from "react";

import { LanguageToggle, ToggleLinkProps } from "./LanguageToggle";

export function Navbar({
  locale,
  logo,
  homeHref,
  navLinks,
  navButtons,
  ...toggleProps
}: ToggleLinkProps & {
  locale: Locale;
  logo: React.ReactNode;
  homeHref: string;
  navLinks: AnchorProps[];
  navButtons: React.ReactNode;
}) {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <nav className="border-b border-dashed border-dark">
      <div className="mx-auto w-full max-w-screen-1.5xl px-4 font-bold">
        <div className="grid grid-cols-[auto_1fr] items-center gap-x-4 py-6 md:grid-cols-[1fr_auto_1fr]">
          <Link href={homeHref}>{logo}</Link>
          <div className="mx-auto hidden h-12 items-center md:flex">
            {navLinks.map(({ href, text }) => (
              <Link key={text} href={href} className="p-2 text-dark">
                {text}
              </Link>
            ))}
          </div>
          <div className="ml-auto flex items-center gap-x-4">
            {navButtons}
            <LanguageToggle current={locale} {...toggleProps} />
            <div className="flex items-center md:hidden">
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
