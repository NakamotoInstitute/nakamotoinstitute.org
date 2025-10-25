import Link from "next/link";

import { Arrow } from "./Arrow";

export type ArrowButtonProps = {
  direction: "left" | "right";
  href?: string;
};

export function ArrowLink({ direction, href }: ArrowButtonProps) {
  return href ? (
    <Link
      className="border-taupe-light inline-flex items-center justify-center rounded-full border p-1.5"
      href={href}
    >
      <Arrow direction={direction} />
    </Link>
  ) : (
    <span className="border-taupe-light bg-taupe-light inline-flex items-center justify-center rounded-full border p-1.5">
      <Arrow direction={direction} />
    </span>
  );
}
