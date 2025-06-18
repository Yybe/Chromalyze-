import AnalysisClient from "./analysis-client"
import { Metadata } from "next"

export const metadata: Metadata = {
  title: "Analysis Results - Chromalyze", // Updated Title
  description: "View your personalized color and style analysis results from Chromalyze." // Updated Description
}

interface PageProps {
  params: {
    id: string;
  };
}

export default function Page({ params }: PageProps) {
  // Log the ID parameter for debugging
  console.log('Page component received ID param:', params.id);
  
  // Ensure we're passing a valid ID
  if (!params.id) {
    console.error('Missing ID in page params');
  }
  
  return <AnalysisClient id={params.id} />;
}
