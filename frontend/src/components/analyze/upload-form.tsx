"use client"

import * as React from "react"
import { useCallback, useState } from "react"
import { useRouter } from "next/navigation"
import { useDropzone } from "react-dropzone"
import { Upload, X, Camera } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { cn } from "@/lib/utils"
import CameraCapture from "@/components/camera/camera-capture"
import { analysisService } from "@/lib/analysis-service"

const BACKEND_URL = 'http://localhost:8000'

export function UploadForm() {
  const router = useRouter()
  const [file, setFile] = useState<File | null>(null)
  const [preview, setPreview] = useState<string | null>(null)
  const [isUploading, setIsUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [error, setError] = useState<string | null>(null)

  const [useEnhancedAnalysis, setUseEnhancedAnalysis] = useState(true)
  const [showCamera, setShowCamera] = useState(false)

  const onDrop = useCallback((acceptedFiles: File[]) => {
    setError(null)
    const selectedFile = acceptedFiles[0]

    // Validate file type
    if (!selectedFile.type.startsWith('image/')) {
      setError('Please upload an image file')
      return
    }

    // Validate file size (5MB limit)
    if (selectedFile.size > 5 * 1024 * 1024) {
      setError('File size should be less than 5MB')
      return
    }

    setFile(selectedFile)
    const objectUrl = URL.createObjectURL(selectedFile)
    setPreview(objectUrl)

    return () => URL.revokeObjectURL(objectUrl)
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.webp']
    },
    maxFiles: 1
  })

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (!file) return

    setIsUploading(true)
    setError(null)

    try {
      if (useEnhancedAnalysis) {
        // Use enhanced local analysis
        await runEnhancedAnalysis()
      } else {
        // Use legacy backend analysis
        await runLegacyAnalysis()
      }
    } catch (error) {
      setIsUploading(false)
      setError(error instanceof Error ? error.message : 'Analysis failed')
    }
  }

  const runEnhancedAnalysis = async () => {
    try {
      // Create image element from file
      const imageElement = await createImageElement(file!)

      // Run comprehensive analysis with automatic saving
      const result = await analysisService.analyzeImage(imageElement, true)

      // Store the photo URL and analysis results
      const analysisId = `enhanced_${Date.now()}`;
      if (preview) {
        sessionStorage.setItem(`photo_${analysisId}`, preview);
      }
      sessionStorage.setItem(`analysis_${analysisId}`, JSON.stringify(result));

      setIsUploading(false)

      // Redirect to the main analysis page which handles the entry screen
      router.push(`/analyze/${analysisId}`)

    } catch (error) {
      console.error('Enhanced analysis failed:', error)
      // Fallback to legacy analysis
      setUseEnhancedAnalysis(false)
      await runLegacyAnalysis()
    }
  }

  const runLegacyAnalysis = async () => {
    const formData = new FormData()
    formData.append('file', file!)

    const response = await fetch(`${BACKEND_URL}/api/upload`, {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      throw new Error(`Upload failed: ${response.statusText}`)
    }

    const data = await response.json()

    if (data.status === 'completed') {
      // Use the actual analysis ID from backend
      const analysisId = data.analysis_id;

      // Store results and photo for the analysis client
      if (preview) {
        sessionStorage.setItem(`photo_${analysisId}`, preview);
      }

      setIsUploading(false)
      router.push(`/analyze/${analysisId}`)
    } else {
      throw new Error(data.error_detail || 'Analysis failed')
    }
  }

  const createImageElement = (file: File): Promise<HTMLImageElement> => {
    return new Promise((resolve, reject) => {
      const img = new Image()
      img.onload = () => resolve(img)
      img.onerror = reject
      img.src = URL.createObjectURL(file)
    })
  }

  const handleRemove = () => {
    setFile(null)
    setPreview(null)
    setError(null)
    setUploadProgress(0)
  }

  const handleCameraCapture = (imageSrc: string) => {
    // Convert base64 to File
    fetch(imageSrc)
      .then(res => res.blob())
      .then(blob => {
        const file = new File([blob], 'camera-capture.jpg', { type: 'image/jpeg' })
        setFile(file)
        setPreview(imageSrc)
        setShowCamera(false)
      })
      .catch(error => {
        setError('Failed to process camera image')
        console.error('Camera capture error:', error)
      })
  }

  // Simulate upload progress
  React.useEffect(() => {
    if (isUploading) {
      // Simulate upload progress
      const interval = setInterval(() => {
        setUploadProgress((prevProgress) => {
          const newProgress = prevProgress + 5;
          return newProgress >= 95 ? 95 : newProgress; // Cap at 95
        });
      }, 100);

      return () => clearInterval(interval);
    } else {
      setUploadProgress(0);
    }
  }, [isUploading]);

  return (
    <div className="w-full max-w-2xl mx-auto">
      {!file ? (
        <div className="space-y-4">
          {/* Drag and Drop Area */}
          <div
            {...getRootProps()}
            className={cn(
              "border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors",
              isDragActive
                ? "border-blue-400 bg-blue-50 dark:bg-blue-900/20"
                : "border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500"
            )}
          >
            <input {...getInputProps()} />
            <Upload className="mx-auto h-12 w-12 text-gray-400 dark:text-gray-500 mb-4" />
            <p className="text-lg font-medium text-gray-900 dark:text-white mb-2">
              Upload your photo
            </p>
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">
              Drag and drop your image here, or click to select
            </p>
            <p className="text-xs text-gray-400 dark:text-gray-500">
              Supports: JPG, PNG, WebP (max 5MB)
            </p>
          </div>

          {/* Divider */}
          <div className="flex items-center justify-center">
            <div className="flex items-center space-x-2 text-gray-500 dark:text-gray-400">
              <div className="h-px bg-gray-300 dark:bg-gray-600 flex-1"></div>
              <span className="text-sm">or</span>
              <div className="h-px bg-gray-300 dark:bg-gray-600 flex-1"></div>
            </div>
          </div>

          {/* Camera Button */}
          <Button
            onClick={() => setShowCamera(true)}
            variant="outline"
            className="w-full"
          >
            <Camera className="h-4 w-4 mr-2" />
            Take Photo with Camera
          </Button>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Preview */}
          {preview && (
            <div className="relative">
              <img
                src={preview}
                alt="Preview"
                className="w-full h-64 object-cover rounded-lg"
              />
              <button
                type="button"
                onClick={handleRemove}
                className="absolute top-2 right-2 p-1 bg-red-500 text-white rounded-full hover:bg-red-600"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
          )}

          {/* Upload Progress */}
          {isUploading && (
            <div className="space-y-2">
              <Progress value={uploadProgress} className="w-full" />
              <p className="text-sm text-gray-600 text-center">
                Analyzing your image... {uploadProgress}%
              </p>
            </div>
          )}

          <Button type="submit" disabled={!file || isUploading} className="w-full">
            {isUploading ? 'Analyzing...' : 'Analyze Image'}
          </Button>
        </form>
      )}

      {error && (
        <div className="mt-4 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-md">
          <p className="text-red-600 dark:text-red-400">{error}</p>
        </div>
      )}



      {/* Camera Capture Modal */}
      {showCamera && (
        <CameraCapture
          onCapture={handleCameraCapture}
          onClose={() => setShowCamera(false)}
        />
      )}
    </div>
  )
}
