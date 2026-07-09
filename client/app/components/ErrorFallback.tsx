"use client";

type ErrorFallbackProps = {
  reset: () => void;
};

export function ErrorFallback({ reset }: ErrorFallbackProps) {
  return (
    <main className="mx-auto my-10 w-full max-w-218 grow px-4 pb-4 md:mt-18">
      <h1 className="mb-6 text-4xl font-medium">Something went wrong</h1>
      <section>
        <p>We could not load this page.</p>
        <button
          className="bg-cardinal hover:bg-crimson mt-4 inline-flex h-10 items-center justify-center px-4 py-3 text-sm font-medium whitespace-nowrap text-white transition-colors"
          type="button"
          onClick={reset}
        >
          Try again
        </button>
      </section>
    </main>
  );
}
