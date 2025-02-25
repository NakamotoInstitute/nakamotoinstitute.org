import Link from "next/link";

import { ArrowLeft } from "./ArrowLeft";
import { ArrowRight } from "./ArrowRight";

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
      {direction === "left" ? <ArrowLeft /> : <ArrowRight />}
    </Link>
  ) : (
    <span className="border-taupe-light bg-taupe-light inline-flex items-center justify-center rounded-full border p-1.5">
      {direction === "left" ? <ArrowLeft /> : <ArrowRight />}
    </span>
  );
}
