// This page has been removed to eliminate duplicate entry screens.
// The entry functionality is now handled by the AnalysisResultsEntry component
// in the main /analyze/[id] route.

'use client';

import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export default function AnalysisEntryPage() {
  const router = useRouter();

  useEffect(() => {
    // Redirect to the main analysis page which handles the entry screen
    const pathSegments = window.location.pathname.split('/');
    const id = pathSegments[pathSegments.length - 2]; // Get ID from /analyze/[id]/entry
    router.replace(`/analyze/${id}`);
  }, [router]);

  return (
    <div className="container flex-1 py-6 md:py-12">
      <div className="mx-auto flex max-w-[800px] flex-col items-center space-y-4">
        <div className="animate-spin w-12 h-12 border-4 border-primary/20 border-t-primary rounded-full"></div>
        <p className="text-muted-foreground">Redirecting...</p>
      </div>
    </div>
  );
}
