import Link from "next/link";

import { BackArrow } from "./BackArrow";

type ReturnButtonProps = {
  className?: string;
  label: string;
  href: string;
};

export function ReturnButton({ className, label, href }: ReturnButtonProps) {
  return (
    <div className={className}>
      <Link className="group flex items-center gap-2" href={href}>
        <BackArrow className="group-hover:stroke-cardinal" />
        <span>{label}</span>
      </Link>
    </div>
  );
}
