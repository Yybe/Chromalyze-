import Link from "next/link"
import { Button } from "@/components/ui/button"

export default function AboutPage() {
  return (
    <div className="container flex-1 py-6 md:py-12">
      <div className="mx-auto flex max-w-[800px] flex-col items-center space-y-8">
        <div className="text-center space-y-4">
          <h1 className="text-3xl font-bold tracking-tight">About Chromalyze</h1> {/* Updated Title */}
          <p className="text-muted-foreground">
            Discover your personalized color season and face shape with our AI-powered analysis tool. {/* Updated Description */}
          </p>
        </div>

        <div className="space-y-6 text-center">
          <section className="space-y-4">
            <h2 className="text-2xl font-semibold">How It Works</h2>
            <div className="grid gap-4 md:grid-cols-3">
              <div className="rounded-lg border p-4">
                <h3 className="font-medium">1. Upload</h3>
                <p className="text-sm text-muted-foreground">
                  Upload a clear photo of your face in good lighting.
                </p>
              </div>
              <div className="rounded-lg border p-4">
                <h3 className="font-medium">2. Analyze</h3>
                <p className="text-sm text-muted-foreground">
                  Our AI analyzes your facial features and skin tone.
                </p>
              </div>
              <div className="rounded-lg border p-4">
                <h3 className="font-medium">3. Results</h3>
                <p className="text-sm text-muted-foreground">
                  Get personalized beauty recommendations.
                </p>
              </div>
            </div>
          </section>

          <section className="space-y-4">
            <h2 className="text-2xl font-semibold">Features</h2>
            <ul className="space-y-2 text-muted-foreground">
              <li>Face shape analysis for makeup and hairstyle recommendations</li>
              <li>Skin tone analysis for your perfect color palette</li>
              <li>Color season determination</li>
              <li>Personalized beauty recommendations</li>
            </ul>
          </section>

          <section className="space-y-4">
            <h2 className="text-2xl font-semibold">Privacy</h2>
            <p className="text-muted-foreground">
              Your privacy is important to us. Uploaded photos are temporarily stored for analysis
              and automatically deleted after processing. We do not share your data with third parties.
            </p>
          </section>

          <div className="pt-4">
            <Button asChild size="lg">
              <Link href="/analyze">Try It Now</Link>
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}
