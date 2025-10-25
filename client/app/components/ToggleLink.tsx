import clsx from "clsx";
import Link from "next/link";
import { UrlObject } from "url";

export type ToggleLinkProps = {
  href: string | UrlObject;
  label: string;
  active: boolean;
};

export async function ToggleLink({ href, label, active }: ToggleLinkProps) {
  return (
    <Link
      className="group hover:bg-sand hover:text-dark flex items-center gap-2 rounded-lg p-1 pr-2"
      href={href}
    >
      <div
        className={clsx(
          "flex w-12 rounded-md p-0.5",
          active
            ? "bg-dandelion justify-end"
            : "bg-sand group-hover:bg-taupe-light",
        )}
      >
        <div className="h-5 w-5.5 rounded-md bg-white drop-shadow-xs"></div>
      </div>
      <span>{label}</span>
    </Link>
  );
}
