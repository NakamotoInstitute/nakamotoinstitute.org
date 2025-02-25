"use client";

import {
  autoUpdate,
  useClick,
  useDismiss,
  useFloating,
  useFocus,
  useInteractions,
} from "@floating-ui/react";
import clsx from "clsx";
import Link from "next/link";
import { useState } from "react";

import { defaultLocale } from "@/i18n";

export type ToggleLinkProps = {
  current?: Locale;
  links?: AnchorProps[];
};

export function LanguageToggle({
  current = defaultLocale,
  links = [],
}: ToggleLinkProps) {
  const [isOpen, setIsOpen] = useState(false);

  const { refs, context, floatingStyles } = useFloating({
    open: isOpen,
    placement: "bottom-end",
    onOpenChange: setIsOpen,
    whileElementsMounted: autoUpdate,
  });

  const click = useClick(context);
  const dismiss = useDismiss(context);
  const focus = useFocus(context);

  const { getReferenceProps, getFloatingProps } = useInteractions([
    click,
    dismiss,
    focus,
  ]);

  return (
    <div>
      <button
        type="button"
        className={clsx(
          "text-dark border-1 px-2.5 py-2 text-sm focus:outline-hidden",
          isOpen && "border-dark",
          !isOpen && "border-transparent",
        )}
        ref={refs.setReference}
        {...getReferenceProps({
          onClick() {
            setIsOpen(!isOpen);
          },
        })}
      >
        <span className="sr-only">Toggle language</span>
        {current.toUpperCase()}
      </button>
      {isOpen ? (
        <div
          className="z-50 mt-3 w-56 rounded-xs bg-white p-2 font-semibold shadow-lg"
          ref={refs.setFloating}
          style={floatingStyles}
          {...getFloatingProps()}
        >
          <ul>
            {links.map((link) => (
              <li key={link.href} className="mb-1 last:mb-0">
                <Link
                  href={link.href}
                  className="hover:bg-cream hover:text-dark block rounded-xs p-3"
                >
                  {link.text}
                </Link>
              </li>
            ))}
          </ul>
        </div>
      ) : null}
    </div>
  );
}
