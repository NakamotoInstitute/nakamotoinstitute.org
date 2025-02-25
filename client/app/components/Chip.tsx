import clsx from "clsx";

type ChipProps = {
  className?: string;
  children: string;
};

export function Chip({ className, children }: ChipProps) {
  return (
    <div
      className={clsx(
        "bg-sand inline-flex items-center rounded-sm border border-transparent px-2.5 py-0.5 pb-1 font-mono text-xs font-semibold transition-colors",
        className,
      )}
    >
      {children}
    </div>
  );
}
