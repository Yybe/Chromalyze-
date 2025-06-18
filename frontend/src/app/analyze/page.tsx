import { UploadForm } from "@/components/analyze/upload-form"

export default function AnalyzePage() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 py-8">
      <div className="container mx-auto px-4 max-w-6xl">
        <div className="text-center mb-8">
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
            Beauty Analysis
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Upload a clear photo to receive detailed analysis of your facial features and personalized beauty recommendations.
          </p>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6 md:p-8">
          <UploadForm />
        </div>
      </div>
    </div>
  )
}