"use client";

import "./globals.css";

import { ErrorFallback } from "@/app/components/ErrorFallback";

type GlobalErrorProps = {
  error: Error & { digest?: string };
  reset: () => void;
};

export default function GlobalError({
  error: _error,
  reset,
}: GlobalErrorProps) {
  return (
    <html lang="en" className="bg-cream text-dark font-serif">
      <body className="flex min-h-screen flex-col">
        <ErrorFallback reset={reset} />
      </body>
    </html>
  );
}
