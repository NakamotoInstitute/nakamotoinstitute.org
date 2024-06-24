import Link from "next/link";

import { BackArrow } from "./BackArrow";

type ReturnButtonProps = {
  className?: string;
  label: string;
  url: string;
};

export function ReturnButton({ className, label, url }: ReturnButtonProps) {
  return (
    <div className={className}>
      <Link
        className="group mb-4 flex items-center gap-2 md:gap-3 md:text-xl"
        href={url}
      >
        <BackArrow className="group-hover:stroke-cardinal" />
        <span>{label}</span>
      </Link>
    </div>
  );
}
