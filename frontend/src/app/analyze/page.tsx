import { UploadForm } from "@/components/analyze/upload-form"

export default function AnalyzePage() {
  return (
    <div className="container flex-1 py-6 md:py-12">
      <div className="mx-auto flex max-w-[800px] flex-col items-center space-y-4">
        <h1 className="text-3xl font-bold tracking-tight">Facial Feature Analysis</h1>
        <p className="text-center text-muted-foreground">
          Upload a clear photo to receive a detailed analysis of your facial characteristics and personalized recommendations.
        </p>
        <div className="w-full">
          <UploadForm />
        </div>
      </div>
    </div>
  )
} 