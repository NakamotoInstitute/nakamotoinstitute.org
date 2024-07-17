type ChipProps = {
  children: string;
};

export function Chip({ children }: ChipProps) {
  return (
    <div className="inline-flex items-center rounded border border-transparent bg-sand px-2.5 py-0.5 pb-1 font-mono text-xs font-semibold transition-colors">
      {children}
    </div>
  );
}
