'use client'

import { Button } from '@/components/ui/button'
import { useRouter } from 'next/navigation'

interface ColorObject {
  name: string;
  hex: string;
}

interface Palette {
  description: string
  recommended: ColorObject[]
  avoid: ColorObject[]
}

interface FaceShapeRecommendations {
  description: string
  strengths: string[]
  hairstyles: {
    recommended: string[]
    avoid: string[]
  }
  makeup: {
    contouring: string
    eyebrows: string
    eyes: string
    lips: string
  }
  accessories: {
    earrings: string
    glasses: string
    hats: string
  }
}

interface AnalysisResult {
  face_shape: string
  color_season: string
  faces_detected?: number
  palette?: Palette
  face_shape_recommendations?: FaceShapeRecommendations
}

export default function ResultsDisplay({ results }: { results: AnalysisResult }) {
  const router = useRouter()

  return (
    <div className="container flex-1 py-6 md:py-12 bg-background">
      <div className="mx-auto flex max-w-[800px] flex-col items-center space-y-8">
        <h1 className="text-3xl font-bold tracking-tight text-foreground font-[Inter]">Analysis Complete</h1>

        {results.faces_detected !== undefined && (
          <div className="w-full text-center">
            <span className="inline-flex items-center rounded-md bg-primary/10 px-2 py-1 text-xs font-medium text-primary ring-1 ring-inset ring-primary/20">
              {results.faces_detected === 0
                ? "No face detected, providing general analysis"
                : results.faces_detected === 1
                  ? "1 face detected"
                  : `${results.faces_detected} faces detected (analyzed primary face)`}
            </span>
          </div>
        )}
        
        <div className="w-full space-y-8">
          {/* Face Shape Section */}
          <div className="rounded-lg border border-border bg-card p-6">
            <h2 className="text-2xl font-semibold mb-4 text-foreground font-[Inter]">Face Shape: {results.face_shape}</h2>

            {results.face_shape_recommendations ? (
              <div className="space-y-6">
                <p className="text-muted-foreground font-[Inter]">
                  {results.face_shape_recommendations.description}
                </p>

                {/* Strengths */}
                <div className="space-y-2">
                  <h3 className="font-medium text-green-600 font-[Inter]">Your Natural Strengths:</h3>
                  <ul className="list-disc pl-5 space-y-1">
                    {results.face_shape_recommendations.strengths.map((strength, i) => (
                      <li key={i} className="text-sm text-green-600 font-[Inter]">{strength}</li>
                    ))}
                  </ul>
                </div>

                {/* Hairstyles */}
                <div className="grid md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <h3 className="font-medium text-blue-700">Recommended Hairstyles:</h3>
                    <ul className="list-disc pl-5 space-y-1">
                      {results.face_shape_recommendations.hairstyles.recommended.slice(0, 4).map((style, i) => (
                        <li key={i} className="text-sm text-blue-600">{style}</li>
                      ))}
                    </ul>
                  </div>

                  <div className="space-y-2">
                    <h3 className="font-medium text-red-700">Hairstyles to Avoid:</h3>
                    <ul className="list-disc pl-5 space-y-1">
                      {results.face_shape_recommendations.hairstyles.avoid.slice(0, 3).map((style, i) => (
                        <li key={i} className="text-sm text-red-600">{style}</li>
                      ))}
                    </ul>
                  </div>
                </div>

                {/* Makeup Tips */}
                <div className="space-y-2">
                  <h3 className="font-medium text-purple-700">Makeup Tips:</h3>
                  <div className="grid md:grid-cols-2 gap-2">
                    <div className="text-sm">
                      <span className="font-medium">Contouring:</span> {results.face_shape_recommendations.makeup.contouring}
                    </div>
                    <div className="text-sm">
                      <span className="font-medium">Eyebrows:</span> {results.face_shape_recommendations.makeup.eyebrows}
                    </div>
                    <div className="text-sm">
                      <span className="font-medium">Eyes:</span> {results.face_shape_recommendations.makeup.eyes}
                    </div>
                    <div className="text-sm">
                      <span className="font-medium">Lips:</span> {results.face_shape_recommendations.makeup.lips}
                    </div>
                  </div>
                </div>

                {/* Accessories */}
                <div className="space-y-2">
                  <h3 className="font-medium text-amber-700">Accessory Recommendations:</h3>
                  <div className="grid md:grid-cols-3 gap-2">
                    <div className="text-sm">
                      <span className="font-medium">Earrings:</span> {results.face_shape_recommendations.accessories.earrings}
                    </div>
                    <div className="text-sm">
                      <span className="font-medium">Glasses:</span> {results.face_shape_recommendations.accessories.glasses}
                    </div>
                    <div className="text-sm">
                      <span className="font-medium">Hats:</span> {results.face_shape_recommendations.accessories.hats}
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="space-y-4">
                <p className="text-muted-foreground mb-4">
                  Your face has characteristics of a {results.face_shape.toLowerCase()} shape.
                </p>

                {/* Fallback recommendations */}
                <div className="space-y-2">
                  <h3 className="font-medium">Basic Recommendations for {results.face_shape} faces:</h3>
                  <ul className="list-disc pl-5 space-y-1">
                    {getFaceShapeRecommendations(results.face_shape).map((rec, i) => (
                      <li key={i} className="text-sm text-muted-foreground">{rec}</li>
                    ))}
                  </ul>
                </div>
              </div>
            )}
          </div>
          
          {/* Color Season Section */}
          <div className="rounded-lg border p-6">
            <h2 className="text-2xl font-semibold mb-4">Color Season: {results.color_season}</h2>
            <p className="text-muted-foreground mb-4">
              Your color analysis indicates you're a {results.color_season} type.
            </p>
            
            {/* Color Palette */}
            {results.palette && (
              <div className="space-y-4">
                <p className="text-sm text-muted-foreground font-[Inter]">{results.palette.description}</p>

                <div className="space-y-2">
                  <h3 className="font-medium text-foreground font-[Inter]">Recommended Colors:</h3>
                  <div className="flex flex-wrap gap-2">
                    {results.palette.recommended.map((color, i) => (
                      <div
                        key={i}
                        className="text-sm py-1 px-3 rounded-full flex items-center gap-1 font-[Inter]"
                        style={{
                          backgroundColor: `${color.hex}20`,
                          color: color.hex,
                          border: `1px solid ${color.hex}40`
                        }}
                      >
                        <span
                          className="inline-block w-3 h-3 rounded-full border border-border"
                          style={{ backgroundColor: color.hex }}
                        ></span>
                        {color.name}
                      </div>
                    ))}
                  </div>
                </div>

                <div className="space-y-2">
                  <h3 className="font-medium text-foreground font-[Inter]">Colors to Avoid:</h3>
                  <div className="flex flex-wrap gap-2">
                    {results.palette.avoid.map((color, i) => (
                      <div
                        key={i}
                        className="text-sm py-1 px-3 rounded-full flex items-center gap-1 text-destructive font-[Inter]"
                        style={{
                          backgroundColor: `${color.hex}10`,
                          border: `1px solid ${color.hex}40`
                        }}
                      >
                        <span
                          className="inline-block w-3 h-3 rounded-full border border-border"
                          style={{ backgroundColor: color.hex }}
                        ></span>
                        {color.name}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
        
        <div className="flex justify-center space-x-4">
          <Button
            onClick={() => router.push('/analyze')}
            className="bg-primary hover:bg-primary/90 text-primary-foreground font-[Inter]"
          >
            New Analysis
          </Button>
          <Button
            variant="outline"
            onClick={() => window.print()}
            className="border-2 hover:bg-secondary/50 font-[Inter]"
          >
            Print Results
          </Button>
        </div>
      </div>
    </div>
  )
}

function getFaceShapeRecommendations(faceShape: string): string[] {
  const recommendations: Record<string, string[]> = {
    'Oval': [
      'Most hairstyles and accessories work well with your balanced proportions',
      'Experiment with different styles as your face shape is versatile',
      'Your face shape is considered ideal for most styles'
    ],
    'Round': [
      'Angular frames and accessories to add definition',
      'Hairstyles with volume at the crown to elongate the face',
      'V-neck tops and vertical patterns to create a slimming effect'
    ],
    'Square': [
      'Oval or round frames to soften angular features',
      'Side-swept bangs and layered hairstyles to soften jawline',
      'Round or curved accessories to balance sharp angles'
    ],
    'Heart': [
      'Bottom-heavy frames or accessories to balance a wider forehead',
      'Hairstyles with volume at the jaw area to create balance',
      'Choker necklaces and V-necks to draw attention away from a narrow chin'
    ],
    'Diamond': [
      'Frames that emphasize the eyes and soften cheekbones',
      'Hairstyles with width at the forehead and jaw to balance pronounced cheekbones',
      'Statement earrings to complement your striking cheekbones'
    ],
    'Oblong': [
      'Horizontal lines and patterns to break up the length of the face',
      'Hairstyles with width at the sides to create the illusion of a wider face',
      'Avoid high necklines and opt for wider necklines instead'
    ],
    'Triangle': [
      'Top-heavy frames and accessories to balance a wider jawline',
      'Hairstyles with volume at the crown to balance a wider jaw',
      'Statement necklaces to draw attention upward from the jaw'
    ]
  }
  
  return recommendations[faceShape] || [
    'Experiment with different styles to find what works best for you',
    'Consider consulting with a professional stylist for personalized recommendations',
    'Balance is key - choose styles that enhance your unique features'
  ]
} 