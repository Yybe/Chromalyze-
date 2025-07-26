'use client';

import React from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ColorDrapingData } from '@/lib/color-draping-types';
import { getTopColors, getAvoidColors, getColorsByCategory } from '@/lib/color-draping-utils';
import { Download, Share2, RotateCcw, Eye, Crown, Palette, CheckCircle, X } from 'lucide-react';
import styles from './summary-screen.module.css';

interface SummaryScreenProps {
  drapingData: ColorDrapingData;
  onDownloadPalette: () => void;
  onShareLookbook: () => void;
  onRestartWalkthrough: () => void;
  onViewFullAnalysis: () => void;
  className?: string;
}

export const SummaryScreen: React.FC<SummaryScreenProps> = ({
  drapingData,
  onDownloadPalette,
  onShareLookbook,
  onRestartWalkthrough,
  onViewFullAnalysis,
  className = ''
}) => {
  const topColors = getTopColors(drapingData, 5);
  const avoidColors = getAvoidColors(drapingData);
  const colorsByCategory = getColorsByCategory(drapingData);

  return (
    <div className={`${styles.summaryScreen} ${className}`}>
      <Card className="max-w-4xl mx-auto shadow-lg">
        <CardContent className="p-8">
          {/* Color Season Header */}
          <div className={styles.seasonHeader}>
            <div className={styles.seasonIcon}>
              <Crown size={40} />
            </div>
            <h1 className={styles.seasonTitle}>
              You are a {drapingData.colorSeason}
            </h1>
            <p className={styles.seasonSubtitle}>
              Your perfect colors have been carefully selected to enhance your natural beauty
            </p>
          </div>

          {/* Top 5 Best Colors */}
          <Card className="mb-8">
            <CardHeader>
              <CardTitle className="flex items-center gap-3 text-2xl">
                <CheckCircle className="text-primary" size={24} />
                Your Top 5 Best Colors
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {topColors.map((color, index) => (
                  <Card key={color.hex} className="relative transition-transform hover:-translate-y-1 hover:shadow-lg">
                    <Badge
                      className="absolute -top-2 -right-2 w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold bg-primary text-primary-foreground"
                    >
                      #{index + 1}
                    </Badge>
                    <CardContent className="p-6">
                      <div
                        className="w-full h-20 rounded-lg mb-4 shadow-md border border-border"
                        style={{ backgroundColor: color.hex }}
                      />
                      <div>
                        <h3 className="text-lg font-semibold text-foreground mb-2 font-[Inter]">{color.name}</h3>
                        <p className="text-sm text-muted-foreground leading-relaxed italic font-[Inter]">{color.feedback}</p>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Full Palette Grid */}
          <Card className="mb-8">
            <CardHeader>
              <CardTitle className="text-2xl">Your Complete Color Palette</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                {Object.entries(colorsByCategory).map(([category, colors]) => {
                  if (category === 'avoid' || colors.length === 0) return null;

                  return (
                    <Card key={category} className="bg-secondary/20">
                      <CardContent className="p-6">
                        <h3 className="text-lg font-semibold text-foreground mb-4 font-[Inter]">
                          {category.charAt(0).toUpperCase() + category.slice(1)} Colors
                        </h3>
                        <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-6 lg:grid-cols-8 gap-4">
                          {colors.map((color) => (
                            <div key={color.hex} className="flex flex-col items-center gap-2">
                              <div
                                className="w-12 h-12 rounded-full shadow-md border-2 border-background"
                                style={{ backgroundColor: color.hex }}
                                title={color.name}
                              />
                              <span className="text-xs text-muted-foreground text-center font-medium font-[Inter]">{color.name}</span>
                            </div>
                          ))}
                        </div>
                      </CardContent>
                    </Card>
                  );
                })}
              </div>
            </CardContent>
          </Card>

          {/* Colors to Avoid */}
          {avoidColors.length > 0 && (
            <Card className="mb-8 border-destructive/20 bg-destructive/5">
              <CardHeader>
                <CardTitle className="flex items-center gap-3 text-2xl text-destructive">
                  <X size={24} />
                  Colors to Avoid
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {avoidColors.map((color) => (
                    <Card key={color.hex} className="opacity-75 border-destructive/20">
                      <CardContent className="p-4">
                        <div
                          className="w-full h-12 rounded-md mb-3 relative shadow-sm border border-border"
                          style={{ backgroundColor: color.hex }}
                        >
                          <div className="absolute inset-0 bg-gradient-to-r from-transparent via-destructive/80 to-transparent transform rotate-45 opacity-60"></div>
                        </div>
                        <div>
                          <h3 className="font-semibold text-foreground mb-1 font-[Inter]">{color.name}</h3>
                          <p className="text-sm text-muted-foreground leading-relaxed italic font-[Inter]">{color.feedback}</p>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Action Buttons */}
          <div className="flex flex-col items-center gap-6 mt-8">
            {/* Primary Action - View Full Analysis */}
            <div className="w-full max-w-md">
              <Button
                size="lg"
                onClick={onViewFullAnalysis}
                className="flex items-center justify-center gap-3 px-8 py-4 w-full bg-gradient-to-r from-primary to-primary/90 hover:from-primary/90 hover:to-primary text-primary-foreground font-semibold transition-all duration-200 hover:shadow-xl min-h-[52px] text-lg"
              >
                <Eye size={22} />
                <span>View Full Analysis</span>
                <span className="text-sm opacity-90">(Face Shape, Accessories & More)</span>
              </Button>
            </div>

            {/* Secondary Actions */}
            <div className="flex flex-col sm:flex-row gap-4 w-full max-w-md">
              <Button
                size="lg"
                onClick={onDownloadPalette}
                className="flex items-center justify-center gap-2 px-6 py-3 bg-green-600 hover:bg-green-700 text-white font-semibold transition-all duration-200 hover:shadow-lg min-h-[44px] w-full sm:w-auto"
              >
                <Download size={18} />
                <span>Download Palette</span>
              </Button>

              <Button
                size="lg"
                onClick={onShareLookbook}
                className="flex items-center justify-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold transition-all duration-200 hover:shadow-lg min-h-[44px] w-full sm:w-auto"
              >
                <Share2 size={18} />
                <span>Share Lookbook</span>
              </Button>
            </div>

            {/* Tertiary Action */}
            <div className="w-full max-w-md">
              <Button
                variant="outline"
                size="default"
                onClick={onRestartWalkthrough}
                className="flex items-center justify-center gap-2 px-4 py-2 w-full font-medium border hover:bg-secondary/50 transition-all duration-200 min-h-[40px]"
              >
                <RotateCcw size={16} />
                <span>Restart Walkthrough</span>
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default SummaryScreen;