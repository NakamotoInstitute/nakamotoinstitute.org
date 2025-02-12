import clsx from "clsx";

type ChipProps = {
  className?: string;
  children: string;
};

export function Chip({ className, children }: ChipProps) {
  return (
    <div
      className={clsx(
        "inline-flex items-center rounded border border-transparent bg-sand px-2.5 py-0.5 pb-1 font-mono text-xs font-semibold transition-colors",
        className,
      )}
    >
      {children}
    </div>
  );
}
