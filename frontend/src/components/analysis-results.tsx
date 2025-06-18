import { User, Palette, Sparkles } from 'lucide-react';

interface AnalysisResultsProps {
  results: any;
}

export function AnalysisResults({ results }: AnalysisResultsProps) {
  if (!results?.result) return null;

  const { face_shape, color_season, features } = results.result;

  return (
    <div className="mt-8 space-y-6">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">Analysis Results</h3>
        
        <div className="space-y-6">
          {/* Face Shape Section */}
          <div className="flex items-start space-x-4">
            <div className="flex-shrink-0">
              <User className="w-6 h-6 text-indigo-600" />
            </div>
            <div>
              <h4 className="text-lg font-medium text-gray-900">Face Shape</h4>
              <p className="mt-1 text-gray-600">{face_shape}</p>
              <div className="mt-2 text-sm text-gray-500">
                <p>This face shape is characterized by:</p>
                <ul className="list-disc list-inside mt-1">
                  {features?.face_shape?.characteristics?.map((char: string, index: number) => (
                    <li key={index}>{char}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>

          {/* Color Season Section */}
          <div className="flex items-start space-x-4">
            <div className="flex-shrink-0">
              <Palette className="w-6 h-6 text-indigo-600" />
            </div>
            <div>
              <h4 className="text-lg font-medium text-gray-900">Color Season</h4>
              <p className="mt-1 text-gray-600">{color_season}</p>
              <div className="mt-2 text-sm text-gray-500">
                <p>Recommended colors for your season:</p>
                <div className="mt-2 flex flex-wrap gap-2">
                  {features?.color_season?.recommended_colors?.map((color: string, index: number) => (
                    <span
                      key={index}
                      className="px-2 py-1 rounded-full text-xs font-medium"
                      style={{
                        backgroundColor: color.toLowerCase(),
                        color: getContrastColor(color),
                      }}
                    >
                      {color}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Additional Features Section */}
          <div className="flex items-start space-x-4">
            <div className="flex-shrink-0">
              <Sparkles className="w-6 h-6 text-indigo-600" />
            </div>
            <div>
              <h4 className="text-lg font-medium text-gray-900">Additional Features</h4>
              <div className="mt-2 space-y-2">
                {features?.additional?.map((feature: any, index: number) => (
                  <div key={index} className="text-sm">
                    <p className="font-medium text-gray-900">{feature.name}</p>
                    <p className="text-gray-600">{feature.description}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Recommendations Section */}
        <div className="mt-6 pt-6 border-t border-gray-200">
          <h4 className="text-lg font-medium text-gray-900 mb-3">Recommendations</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-gray-50 p-4 rounded-lg">
              <h5 className="font-medium text-gray-900 mb-2">Hairstyle Suggestions</h5>
              <ul className="list-disc list-inside text-sm text-gray-600">
                {features?.recommendations?.hairstyles?.map((style: string, index: number) => (
                  <li key={index}>{style}</li>
                ))}
              </ul>
            </div>
            <div className="bg-gray-50 p-4 rounded-lg">
              <h5 className="font-medium text-gray-900 mb-2">Accessory Tips</h5>
              <ul className="list-disc list-inside text-sm text-gray-600">
                {features?.recommendations?.accessories?.map((tip: string, index: number) => (
                  <li key={index}>{tip}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// Helper function to determine text color based on background
function getContrastColor(hexColor: string): string {
  // Remove the # if present
  const color = hexColor.replace('#', '');
  
  // Convert to RGB
  const r = parseInt(color.substr(0, 2), 16);
  const g = parseInt(color.substr(2, 2), 16);
  const b = parseInt(color.substr(4, 2), 16);
  
  // Calculate luminance
  const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
  
  // Return black or white based on luminance
  return luminance > 0.5 ? '#000000' : '#FFFFFF';
} 