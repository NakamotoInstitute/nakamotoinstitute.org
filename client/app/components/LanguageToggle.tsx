"use client";

import {
  autoUpdate,
  useClick,
  useDismiss,
  useFloating,
  useFocus,
  useInteractions,
} from "@floating-ui/react";
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
        className="border-1 border-dark px-2.5 py-2 text-sm text-dark focus:outline-none"
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
          className="z-50 mt-3 w-56 rounded-sm bg-white p-2 font-semibold shadow-lg"
          ref={refs.setFloating}
          style={floatingStyles}
          {...getFloatingProps()}
        >
          <ul>
            {links.map((link) => (
              <li key={link.href} className="mb-1 last:mb-0">
                <Link
                  href={link.href}
                  className="block rounded-sm p-3 hover:bg-cream hover:text-dark"
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
