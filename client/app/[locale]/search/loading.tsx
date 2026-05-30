const TAB_WIDTHS = ["w-10", "w-24", "w-16", "w-20", "w-20"];
const ROW_COUNT = 6;

// RootLayout renders <html> only; the page supplies <body> (via PageLayout), so
// this loading fallback must render <body> too — otherwise its markup is an
// invalid child of <html> and React reports a hydration error.
export default function SearchLoading() {
  return (
    <body className="flex min-h-screen flex-col">
      <div
        className="mx-auto my-10 w-full max-w-240 grow px-4 pb-4 md:mt-18"
        aria-hidden="true"
      >
        {/* Page heading */}
        <div className="bg-taupe-light/60 mb-4 h-9 w-32 animate-pulse rounded" />

        {/* Search box */}
        <div className="bg-taupe-light/60 mb-6 h-12 w-full max-w-xl animate-pulse rounded-xs" />

        {/* Tab bar */}
        <div className="border-taupe-light mb-6 flex flex-wrap gap-x-4 gap-y-2 border-b border-dashed pb-3">
          {TAB_WIDTHS.map((w, i) => (
            <div
              key={i}
              className={`bg-taupe-light/60 h-4 animate-pulse rounded ${w}`}
            />
          ))}
        </div>

        {/* Result rows */}
        <div>
          {Array.from({ length: ROW_COUNT }).map((_, i) => (
            <div
              key={i}
              className="border-taupe-light border-t border-dashed py-4 first:border-t-0"
            >
              <div className="bg-taupe-light/60 h-5 w-3/4 animate-pulse rounded" />
              <div className="bg-taupe-light/40 mt-2 h-4 w-full animate-pulse rounded" />
              <div className="bg-taupe-light/40 mt-1 h-4 w-5/6 animate-pulse rounded" />
              <div className="bg-taupe-light/30 mt-2 h-3 w-32 animate-pulse rounded" />
            </div>
          ))}
        </div>
      </div>
    </body>
  );
}
