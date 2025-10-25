import Link from "next/link";

import { Arrow } from "./Arrow";

type ReturnButtonProps = {
  className?: string;
  label: string;
  href: string;
};

export function ReturnButton({ className, label, href }: ReturnButtonProps) {
  return (
    <div className={className}>
      <Link className="group flex items-center gap-2" href={href}>
        <Arrow direction="back" className="group-hover:stroke-cardinal" />
        <span>{label}</span>
      </Link>
    </div>
  );
}
