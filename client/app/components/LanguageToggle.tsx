"use client";

import { useState } from "react";
import Link from "next/link";
import {
  autoUpdate,
  useClick,
  useFloating,
  useInteractions,
  useDismiss,
  useFocus,
} from "@floating-ui/react";

type LanguageLink = { name: string; href: string };

export type ToggleLinkProps = {
  current?: string;
  links?: LanguageLink[];
};

export function LanguageToggle({
  current = "English",
  links = [],
}: ToggleLinkProps) {
  const [isOpen, setIsOpen] = useState(false);

  const { refs, context, floatingStyles } = useFloating({
    open: isOpen,
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
        className="p-1 text-sm focus:outline-none"
        ref={refs.setReference}
        {...getReferenceProps({
          onClick() {
            setIsOpen(!isOpen);
          },
        })}
      >
        <span className="sr-only">Toggle language</span>
        {current}
      </button>
      {isOpen ? (
        <div
          className="bg-bone rounded-sm p-2 text-sm shadow-lg"
          ref={refs.setFloating}
          style={floatingStyles}
          {...getFloatingProps()}
        >
          <ul>
            {links.map((link) => (
              <li key={link.href} className="mb-1 last:mb-0">
                <Link href={link.href} className="text-night">
                  {link.name}
                </Link>
              </li>
            ))}
          </ul>
        </div>
      ) : null}
    </div>
  );
}
