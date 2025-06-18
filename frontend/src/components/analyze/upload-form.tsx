"use client"

import * as React from "react"
import { useCallback, useState } from "react"
import { useDropzone } from "react-dropzone"
import { Upload, X } from "lucide-react"
import Image from "next/image"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { cn } from "@/lib/utils"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"

const BACKEND_URL = 'http://localhost:8000'

interface UploadResponse {
  analysis_id: string
}

interface AnalysisResponse {
  status: string
  result: {
    face_shape: string
    color_season: string
    note?: string
  }
}

export function UploadForm() {
  const [file, setFile] = useState<File | null>(null)
  const [preview, setPreview] = useState<string | null>(null)
  const [isUploading, setIsUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [error, setError] = useState<string | null>(null)
  const [results, setResults] = useState<AnalysisResponse | null>(null)
  const router = useRouter()

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
    setResults(null)

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch(`${BACKEND_URL}/api/upload`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error(`Upload failed: ${response.statusText}`)
      }

      const data = await response.json()
      
      if (data.status === 'completed') {
        setIsUploading(false)
        setResults(data)
      } else {
        throw new Error(data.error_detail || 'Analysis failed')
      }

    } catch (error) {
      setIsUploading(false)
      setError(error instanceof Error ? error.message : 'Upload failed')
    }
  }

  const handleRemove = () => {
    setFile(null)
    setPreview(null)
    setError(null)
    setUploadProgress(0)
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
    <div className="w-full max-w-md mx-auto">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="image">Upload Image</Label>
          <Input
            id="image"
            type="file"
            accept="image/*"
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setFile(e.target.files?.[0] || null)}
            className="w-full"
          />
        </div>
        
        <Button type="submit" disabled={!file || isUploading} className="w-full">
          {isUploading ? 'Analyzing...' : 'Analyze Image'}
        </Button>
      </form>

      {error && (
        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-md">
          <p className="text-red-600">{error}</p>
        </div>
      )}

      {results && (
        <div className="mt-8 space-y-4">
          <div className="p-4 bg-green-50 border border-green-200 rounded-md">
            <h3 className="text-lg font-semibold text-green-800">Analysis Results</h3>
            <div className="mt-2 space-y-2">
              <p><strong>Face Shape:</strong> {results.result.face_shape}</p>
              <p><strong>Color Season:</strong> {results.result.color_season}</p>
              {results.result.note && (
                <p className="text-sm text-green-600">{results.result.note}</p>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
