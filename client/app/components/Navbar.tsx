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
    <nav className="border-dark border-b border-dashed">
      <div className="max-w-[theme(screens.1.5xl)] mx-auto w-full px-4 font-bold">
        <div className="grid grid-cols-[auto_1fr] items-center gap-x-4 py-6 md:grid-cols-[1fr_auto_1fr]">
          <div>
            <div className="max-w-fit">
              <Link className="max-w-fit" href={homeHref}>
                {logo}
              </Link>
            </div>
          </div>
          <div className="mx-auto hidden h-12 items-center md:flex">
            {navLinks.map(({ href, text }) => (
              <Link
                key={text}
                href={href}
                className="text-dark hover:text-cardinal active:text-cardinal p-2"
              >
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
                className="inline-flex cursor-pointer items-center justify-center rounded-md p-2 focus:ring-2 focus:outline-hidden focus:ring-inset"
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
        <div className="space-y-1 px-2 pt-2 pb-3">
          {navLinks.map(({ href, text }) => (
            <Link
              key={text}
              href={href}
              className="text-dark hover:text-cardinal active:text-cardinal block px-3 py-2"
            >
              {text}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  );
}
