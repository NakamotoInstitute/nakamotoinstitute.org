type ChipProps = {
  children: string;
};

export function Chip({ children }: ChipProps) {
  return (
    <div className="focus:ring-ring inline-flex items-center rounded-full border border-transparent bg-blue-600 px-2.5 py-0.5 pb-1 font-mono text-xs font-semibold text-white transition-colors hover:bg-blue-600/80 focus:outline-none focus:ring-2 focus:ring-offset-2">
      {children}
    </div>
  );
}
