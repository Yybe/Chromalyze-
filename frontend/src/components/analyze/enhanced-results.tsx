'use client';

import React from 'react';
import { ComprehensiveAnalysisResult } from '@/lib/analysis-service';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import {
  User,
  Palette,
  Scissors,
  Glasses,
  Heart,
  Clock,
  Star,
  TrendingUp
} from 'lucide-react';
import { generateColorName } from '@/lib/color-name-generator';

interface EnhancedResultsProps {
  results: ComprehensiveAnalysisResult;
}

const EnhancedResults: React.FC<EnhancedResultsProps> = ({ results }) => {
  const { faceShape, colorSeason, recommendations, confidence, processingTime } = results;

  return (
    <div className="w-full max-w-4xl mx-auto space-y-6">
      {/* Clean Header Summary */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-xl text-gray-900 dark:text-white">
            <Star className="h-6 w-6 text-blue-600 dark:text-blue-400" />
            Your Analysis Results
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center p-6 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
              <User className="h-12 w-12 mx-auto mb-3 text-blue-600 dark:text-blue-400" />
              <h3 className="font-semibold text-lg text-gray-900 dark:text-white">Face Shape</h3>
              <p className="text-2xl font-bold capitalize text-blue-700 dark:text-blue-400 mt-2">{faceShape.faceShape}</p>
              <Badge variant="secondary" className="mt-2">
                {Math.round(faceShape.confidence * 100)}% confidence
              </Badge>
            </div>
            <div className="text-center p-6 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
              <Palette className="h-12 w-12 mx-auto mb-3 text-purple-600 dark:text-purple-400" />
              <h3 className="font-semibold text-lg text-gray-900 dark:text-white">Color Season</h3>
              <p className="text-2xl font-bold capitalize text-purple-700 dark:text-purple-400 mt-2">
                {colorSeason.season.replace('_', ' ')}
              </p>
              <Badge variant="secondary" className="mt-2">
                {Math.round(colorSeason.confidence * 100)}% confidence
              </Badge>
            </div>
            <div className="text-center p-6 bg-green-50 dark:bg-green-900/20 rounded-lg">
              <Clock className="h-12 w-12 mx-auto mb-3 text-green-600 dark:text-green-400" />
              <h3 className="font-semibold text-lg text-gray-900 dark:text-white">Processing Time</h3>
              <p className="text-2xl font-bold text-green-700 dark:text-green-400 mt-2">{Math.round(processingTime)}ms</p>
              <Badge variant="secondary" className="mt-2">
                Overall: {Math.round(confidence * 100)}%
              </Badge>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Clean Analysis Tabs */}
      <Tabs defaultValue="overview" className="w-full">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="hairstyles">Hairstyles</TabsTrigger>
          <TabsTrigger value="colors">Colors</TabsTrigger>
          <TabsTrigger value="accessories">Accessories</TabsTrigger>
          <TabsTrigger value="styling">Styling</TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-6 mt-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <User className="h-5 w-5" />
                  Face Shape Analysis
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <p className="font-semibold text-xl capitalize text-blue-700 dark:text-blue-400">
                    {faceShape.faceShape} Face
                  </p>
                  <Progress value={faceShape.confidence * 100} className="mt-2" />
                  <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                    {Math.round(faceShape.confidence * 100)}% confidence
                  </p>
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-300 space-y-2">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <p className="font-medium">Face Ratio:</p>
                      <p className="text-gray-800 dark:text-gray-200">{faceShape.measurements.faceRatio.toFixed(2)}</p>
                    </div>
                    <div>
                      <p className="font-medium">Jaw Width:</p>
                      <p className="text-gray-800 dark:text-gray-200">{Math.round(faceShape.measurements.jawWidth)}px</p>
                    </div>
                    <div>
                      <p className="font-medium">Forehead:</p>
                      <p className="text-gray-800 dark:text-gray-200">{Math.round(faceShape.measurements.foreheadWidth)}px</p>
                    </div>
                    <div>
                      <p className="font-medium">Cheekbones:</p>
                      <p className="text-gray-800 dark:text-gray-200">{Math.round(faceShape.measurements.cheekboneWidth)}px</p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Palette className="h-5 w-5" />
                  Color Season Analysis
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <p className="font-semibold text-xl capitalize text-purple-700 dark:text-purple-400">
                    {colorSeason.season.replace('_', ' ')}
                  </p>
                  <Progress value={colorSeason.confidence * 100} className="mt-2" />
                  <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                    {Math.round(colorSeason.confidence * 100)}% confidence
                  </p>
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-300 space-y-2">
                  <div>
                    <p className="font-medium">Undertone:</p>
                    <p className="text-gray-800 dark:text-gray-200 capitalize">{colorSeason.undertone}</p>
                  </div>
                  <div>
                    <p className="font-medium">Contrast:</p>
                    <p className="text-gray-800 dark:text-gray-200">{Math.round(colorSeason.contrast * 100)}%</p>
                  </div>
                  <div>
                    <p className="font-medium">Lightness:</p>
                    <p className="text-gray-800 dark:text-gray-200">{Math.round(colorSeason.lightness)}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Hairstyles Tab */}
        <TabsContent value="hairstyles" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Scissors className="h-5 w-5" />
                Recommended Hairstyles
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {recommendations.hairstyles.map((hairstyle, index) => (
                  <div key={index} className="border rounded-lg p-4">
                    <h4 className="font-semibold mb-2">{hairstyle.name}</h4>
                    <p className="text-sm text-gray-600 mb-3">{hairstyle.description}</p>
                    <div className="flex items-center justify-between">
                      <Progress value={hairstyle.suitability * 100} className="flex-1 mr-2" />
                      <span className="text-sm font-medium">{Math.round(hairstyle.suitability * 100)}%</span>
                    </div>
                    <div className="flex flex-wrap gap-1 mt-2">
                      {hairstyle.tags.map((tag, tagIndex) => (
                        <Badge key={tagIndex} variant="outline" className="text-xs">
                          {tag}
                        </Badge>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Colors Tab */}
        <TabsContent value="colors" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Palette className="h-5 w-5" />
                Your Color Palette
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                <div>
                  <h4 className="font-semibold mb-3">Best Colors</h4>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                    {recommendations.colors.primary.map((color, index) => (
                      <div key={index} className="text-center">
                        <div 
                          className="w-full h-12 rounded-lg border mb-1"
                          style={{ backgroundColor: color }}
                        ></div>
                        <div className="text-xs space-y-1">
                          <div className="font-medium">{generateColorName(color)}</div>
                          <div className="text-gray-500">{color}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <h4 className="font-semibold mb-3">Secondary Colors</h4>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                    {recommendations.colors.secondary.map((color, index) => (
                      <div key={index} className="text-center">
                        <div 
                          className="w-full h-12 rounded-lg border mb-1"
                          style={{ backgroundColor: color }}
                        ></div>
                        <div className="text-xs space-y-1">
                          <div className="font-medium">{generateColorName(color)}</div>
                          <div className="text-gray-500">{color}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <h4 className="font-semibold mb-3">Neutrals</h4>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                    {recommendations.colors.neutrals.map((color, index) => (
                      <div key={index} className="text-center">
                        <div 
                          className="w-full h-12 rounded-lg border mb-1"
                          style={{ backgroundColor: color }}
                        ></div>
                        <div className="text-xs space-y-1">
                          <div className="font-medium">{generateColorName(color)}</div>
                          <div className="text-gray-500">{color}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <h4 className="font-semibold mb-3 text-red-600">Colors to Avoid</h4>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                    {recommendations.colors.avoid.map((color, index) => (
                      <div key={index} className="text-center opacity-60">
                        <div 
                          className="w-full h-12 rounded-lg border mb-1 relative"
                          style={{ backgroundColor: color }}
                        >
                          <div className="absolute inset-0 flex items-center justify-center">
                            <div className="w-full h-0.5 bg-red-500 rotate-45"></div>
                          </div>
                        </div>
                        <div className="text-xs space-y-1">
                          <div className="font-medium">{generateColorName(color)}</div>
                          <div className="text-gray-500">{color}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Accessories Tab */}
        <TabsContent value="accessories" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Glasses className="h-5 w-5" />
                Accessory Recommendations
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                {recommendations.accessories.map((accessory, index) => (
                  <div key={index}>
                    <h4 className="font-semibold mb-3 capitalize">{accessory.type}</h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <h5 className="text-sm font-medium text-green-600 mb-2">Recommended</h5>
                        <ul className="text-sm space-y-1">
                          {accessory.recommendations.map((rec, recIndex) => (
                            <li key={recIndex} className="flex items-center gap-2">
                              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                              {rec}
                            </li>
                          ))}
                        </ul>
                      </div>
                      <div>
                        <h5 className="text-sm font-medium text-red-600 mb-2">Avoid</h5>
                        <ul className="text-sm space-y-1">
                          {accessory.avoid.map((avoid, avoidIndex) => (
                            <li key={avoidIndex} className="flex items-center gap-2">
                              <div className="w-2 h-2 bg-red-500 rounded-full"></div>
                              {avoid}
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Styling Tab */}
        <TabsContent value="styling" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Heart className="h-5 w-5" />
                Styling Tips
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                <div>
                  <h4 className="font-semibold mb-3">Necklines</h4>
                  <ul className="text-sm space-y-1">
                    {recommendations.styling.necklines.map((tip, index) => (
                      <li key={index} className="flex items-center gap-2">
                        <TrendingUp className="w-3 h-3 text-blue-500" />
                        {tip}
                      </li>
                    ))}
                  </ul>
                </div>

                <div>
                  <h4 className="font-semibold mb-3">General Styling</h4>
                  <ul className="text-sm space-y-1">
                    {recommendations.styling.general.map((tip, index) => (
                      <li key={index} className="flex items-center gap-2">
                        <TrendingUp className="w-3 h-3 text-purple-500" />
                        {tip}
                      </li>
                    ))}
                  </ul>
                </div>

                <div>
                  <h4 className="font-semibold mb-3">Makeup Recommendations</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <h5 className="text-sm font-medium mb-2">Lip Colors</h5>
                      <ul className="text-sm space-y-1">
                        {recommendations.makeup.lipColors.map((color, index) => (
                          <li key={index}>{color}</li>
                        ))}
                      </ul>
                    </div>
                    <div>
                      <h5 className="text-sm font-medium mb-2">Eye Colors</h5>
                      <ul className="text-sm space-y-1">
                        {recommendations.makeup.eyeColors.map((color, index) => (
                          <li key={index}>{color}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default EnhancedResults;
