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

export type ToggleLinkProps = {
  current?: string;
  links?: AnchorProps[];
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
        className="rounded border-1 border-dark px-3 py-2 text-sm text-dark focus:outline-none"
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
          className="rounded-sm bg-cream p-2 text-sm shadow-lg"
          ref={refs.setFloating}
          style={floatingStyles}
          {...getFloatingProps()}
        >
          <ul>
            {links.map((link) => (
              <li key={link.href} className="mb-1 last:mb-0">
                <Link href={link.href} className="text-dark hover:text-dark">
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
