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
      className="group flex items-center gap-2 rounded-lg p-1 pr-2 hover:bg-sand hover:text-dark"
      href={href}
    >
      <div
        className={clsx(
          "w-12 rounded-md p-0.5",
          active ? "bg-dandelion" : "bg-sand group-hover:bg-taupe-light",
        )}
      >
        <div className="h-5 w-[1.375rem] rounded-md bg-white drop-shadow-sm"></div>
      </div>
      <span>{label}</span>
    </Link>
  );
}
