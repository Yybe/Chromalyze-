'use client';

import React from 'react';
import { Button } from '@/components/ui/button';
import { ColorDrapingData } from '@/lib/color-draping-types';
import { getTopColors, getAvoidColors, getColorsByCategory } from '@/lib/color-draping-utils';
import { Download, Share2, RotateCcw, Eye, Crown, Palette } from 'lucide-react';
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
      <div className={styles.summaryContent}>
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
        <div className="mb-12">
          <h2 className="flex items-center gap-3 text-2xl font-semibold text-gray-900 mb-6">
            <Palette className="text-blue-600" size={24} />
            Your Top 5 Best Colors
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {topColors.map((color, index) => (
              <div key={color.hex} className="bg-gray-50 rounded-xl p-6 relative transition-transform hover:-translate-y-1">
                <div className="absolute -top-3 -right-3 w-8 h-8 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-full flex items-center justify-center text-sm font-semibold shadow-lg">
                  #{index + 1}
                </div>
                <div 
                  className="w-full h-20 rounded-lg mb-4 shadow-md"
                  style={{ backgroundColor: color.hex }}
                />
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">{color.name}</h3>
                  <p className="text-sm text-gray-600 leading-relaxed italic">{color.feedback}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Full Palette Grid */}
        <div className="mb-12">
          <h2 className="text-2xl font-semibold text-gray-900 mb-6">Your Complete Color Palette</h2>
          <div className="space-y-8">
            {Object.entries(colorsByCategory).map(([category, colors]) => {
              if (category === 'avoid' || colors.length === 0) return null;
              
              return (
                <div key={category} className="bg-gray-50 rounded-xl p-6">
                  <h3 className="text-lg font-semibold text-gray-700 mb-4">
                    {category.charAt(0).toUpperCase() + category.slice(1)} Colors
                  </h3>
                  <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-6 lg:grid-cols-8 gap-4">
                    {colors.map((color) => (
                      <div key={color.hex} className="flex flex-col items-center gap-2">
                        <div 
                          className="w-12 h-12 rounded-full shadow-md border-2 border-white"
                          style={{ backgroundColor: color.hex }}
                          title={color.name}
                        />
                        <span className="text-xs text-gray-600 text-center font-medium">{color.name}</span>
                      </div>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Colors to Avoid */}
        {avoidColors.length > 0 && (
          <div className="mb-12 bg-red-50 rounded-xl p-6">
            <h2 className="text-2xl font-semibold text-red-600 mb-6">Colors to Avoid</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {avoidColors.map((color) => (
                <div key={color.hex} className="bg-white rounded-lg p-4 opacity-75 border border-red-200">
                  <div 
                    className="w-full h-12 rounded-md mb-3 relative shadow-sm"
                    style={{ backgroundColor: color.hex }}
                  >
                    <div className="absolute inset-0 bg-gradient-to-r from-transparent via-red-500/80 to-transparent transform rotate-45 opacity-60"></div>
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900 mb-1">{color.name}</h3>
                    <p className="text-sm text-gray-600 leading-relaxed italic">{color.feedback}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex flex-col items-center gap-6">
          <div className="flex flex-col sm:flex-row gap-4">
            <Button
              size="lg"
              onClick={onDownloadPalette}
              className="flex items-center gap-2 px-8 py-3 bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white font-semibold rounded-full transition-all duration-200 hover:-translate-y-0.5 hover:shadow-lg"
            >
              <Download size={20} />
              <span>Download Palette</span>
            </Button>

            <Button
              size="lg"
              onClick={onShareLookbook}
              className="flex items-center gap-2 px-8 py-3 bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-semibold rounded-full transition-all duration-200 hover:-translate-y-0.5 hover:shadow-lg"
            >
              <Share2 size={20} />
              <span>Share Lookbook</span>
            </Button>
          </div>

          <div className="flex flex-col sm:flex-row gap-4">
            <Button
              variant="outline"
              size="lg"
              onClick={onRestartWalkthrough}
              className="flex items-center gap-2 px-6 py-3 font-medium rounded-full border-2 border-gray-300 hover:border-gray-400 hover:bg-gray-50 transition-all duration-200 hover:-translate-y-0.5"
            >
              <RotateCcw size={18} />
              <span>Restart Walkthrough</span>
            </Button>

            <Button
              variant="outline"
              size="lg"
              onClick={onViewFullAnalysis}
              className="flex items-center gap-2 px-6 py-3 font-medium rounded-full border-2 border-gray-300 hover:border-gray-400 hover:bg-gray-50 transition-all duration-200 hover:-translate-y-0.5"
            >
              <Eye size={18} />
              <span>View Full Analysis</span>
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SummaryScreen;