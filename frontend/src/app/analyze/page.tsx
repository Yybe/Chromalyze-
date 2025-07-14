import { UploadForm } from "@/components/analyze/upload-form"

export default function AnalyzePage() {
  return (
    <div className="min-h-screen bg-background py-8">
      <div className="container mx-auto px-4 max-w-6xl">
        <div className="text-center mb-8">
          <h1 className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-primary to-purple-600 bg-clip-text text-transparent mb-4">
            Face Analysis
          </h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Upload a clear photo to receive detailed analysis of your facial features and personalized recommendations.
          </p>
        </div>
        <div className="bg-card rounded-lg shadow-sm border p-6 md:p-8">
          <UploadForm />
        </div>
      </div>
    </div>
  )
}