import Link from "next/link"
import { Button } from "@/components/ui/button"
import { ArrowRight, Camera, Palette, User, CheckCircle } from "lucide-react"

export default function Home() {
  return (
    <div className="min-h-screen bg-white dark:bg-gray-900">
      {/* Clean Hero Section */}
      <section className="py-20 lg:py-32">
        <div className="container mx-auto px-4 max-w-6xl">
          <div className="text-center space-y-8">

            <div className="space-y-4">
              <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold bg-gradient-to-r from-primary to-purple-600 bg-clip-text text-transparent leading-tight">
                Advanced Face Analysis
              </h1>
              <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
                Get precise face shape analysis and personalized color recommendations using cutting-edge AI technology.
                Trusted by professionals and individuals worldwide.
              </p>
            </div>

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/analyze">
                <Button size="lg" className="bg-primary hover:bg-primary/90 text-primary-foreground px-8 py-3">
                  Start Analysis
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <Link href="/about">
                <Button variant="outline" size="lg" className="px-8 py-3">
                  Learn More
                </Button>
              </Link>
            </div>

          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-muted/50">
        <div className="container mx-auto px-4 max-w-6xl">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-foreground mb-4">
              Advanced Analysis Features
            </h2>
            <p className="text-lg text-muted-foreground">
              Comprehensive face analysis powered by cutting-edge AI technology
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center p-6">
              <div className="w-16 h-16 bg-primary/10 rounded-lg flex items-center justify-center mx-auto mb-4">
                <User className="h-8 w-8 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-3 text-foreground">Face Shape Analysis</h3>
              <p className="text-muted-foreground">
                Precise face shape detection using advanced geometric analysis for personalized recommendations.
              </p>
            </div>

            <div className="text-center p-6">
              <div className="w-16 h-16 bg-primary/10 rounded-lg flex items-center justify-center mx-auto mb-4">
                <Palette className="h-8 w-8 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-3 text-foreground">Color Season Analysis</h3>
              <p className="text-muted-foreground">
                Determine your optimal color palette based on skin tone, hair color, and eye color analysis.
              </p>
            </div>

            <div className="text-center p-6">
              <div className="w-16 h-16 bg-primary/10 rounded-lg flex items-center justify-center mx-auto mb-4">
                <CheckCircle className="h-8 w-8 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-3 text-foreground">Personalized Recommendations</h3>
              <p className="text-muted-foreground">
                Get tailored suggestions for hairstyles, makeup, accessories, and styling based on your analysis.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-16 bg-white dark:bg-gray-900">
        <div className="container mx-auto px-4 max-w-6xl">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
              How It Works
            </h2>
            <p className="text-lg text-gray-600 dark:text-gray-300">
              Simple, fast, and accurate analysis in three steps
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-12 h-12 bg-blue-600 dark:bg-blue-500 text-white rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                1
              </div>
              <h3 className="text-xl font-semibold mb-3 text-gray-900 dark:text-white">Upload Photo</h3>
              <p className="text-gray-600 dark:text-gray-300">
                Upload a clear, well-lit photo of your face or take one with your camera.
              </p>
            </div>

            <div className="text-center">
              <div className="w-12 h-12 bg-blue-600 dark:bg-blue-500 text-white rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                2
              </div>
              <h3 className="text-xl font-semibold mb-3 text-gray-900 dark:text-white">AI Analysis</h3>
              <p className="text-gray-600 dark:text-gray-300">
                Our AI analyzes your facial features and determines your face shape and color season.
              </p>
            </div>

            <div className="text-center">
              <div className="w-12 h-12 bg-blue-600 dark:bg-blue-500 text-white rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                3
              </div>
              <h3 className="text-xl font-semibold mb-3 text-gray-900 dark:text-white">Get Results</h3>
              <p className="text-gray-600 dark:text-gray-300">
                Receive detailed analysis results with personalized beauty recommendations.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-gradient-to-r from-primary to-purple-600">
        <div className="container mx-auto px-4 max-w-4xl text-center">
          <h2 className="text-3xl font-bold text-primary-foreground mb-4">
            Ready to Discover Your Face Analysis?
          </h2>
          <p className="text-xl text-primary-foreground/80 mb-8">
            Join thousands of users who have discovered their personalized face analysis and recommendations.
          </p>
          <Link href="/analyze">
            <Button size="lg" className="bg-background text-foreground hover:bg-background/90 px-8 py-3">
              Start Your Analysis Now
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
          </Link>
        </div>
      </section>

    </div>
  )
}
