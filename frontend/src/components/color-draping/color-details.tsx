'use client';

import React from 'react';
import { DrapingColor } from '@/lib/color-draping-types';
import { Check, X } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';

interface ColorDetailsProps {
  color: DrapingColor;
  isVisible: boolean;
  className?: string;
}

export const ColorDetails: React.FC<ColorDetailsProps> = ({
  color,
  isVisible,
  className = ''
}) => {
  const VerdictIcon = color.verdict === 'best' ? Check : X;

  // Get impact-oriented feedback messages
  const getAssessmentText = () => {
    if (color.verdict === 'best') {
      return 'Perfect Match!';
    } else {
      return 'Not Recommended';
    }
  };

  const getDetailedExplanation = () => {
    if (color.verdict === 'best') {
      return color.feedback || 'This shade illuminates your complexion and enhances your natural features.';
    } else {
      return color.feedback || 'This tone drains your natural vitality and creates a tired, washed-out appearance.';
    }
  };

  return (
    <div className={`h-full flex flex-col justify-center space-y-6 transition-all duration-500 ${isVisible ? 'opacity-100 translate-x-0' : 'opacity-0 translate-x-4'} ${className}`}>

      {/* Color Name - Prominent */}
      <div className="text-center">
        <h1 className="text-3xl font-bold text-foreground leading-tight font-[Inter] mb-4">
          {color.name}
        </h1>

        {/* Visual Color Swatch */}
        <div className="flex justify-center mb-6">
          <div
            className="w-16 h-16 rounded-full shadow-lg border-4 border-background"
            style={{ backgroundColor: color.hex }}
          />
        </div>
      </div>

      {/* Instant Visual Feedback Icon */}
      <div className="text-center">
        <div className={`inline-flex items-center justify-center w-20 h-20 rounded-full shadow-lg transition-all duration-300 mb-4 ${
          color.verdict === 'best'
            ? 'bg-green-50 dark:bg-green-900/20 border-2 border-green-500'
            : 'bg-red-50 dark:bg-red-900/20 border-2 border-red-500'
        }`}>
          <VerdictIcon
            size={40}
            className={color.verdict === 'best' ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}
          />
        </div>

        {/* Concise Assessment */}
        <h2 className={`text-2xl font-bold font-[Inter] mb-2 ${
          color.verdict === 'best' ? 'text-green-700 dark:text-green-300' : 'text-red-700 dark:text-red-300'
        }`}>
          {getAssessmentText()}
        </h2>
      </div>

      {/* Detailed Explanation - Impact-Oriented */}
      <Card className="bg-muted/30 border-0">
        <CardContent className="p-6 text-center">
          <p className="text-lg leading-relaxed text-muted-foreground font-[Inter]">
            {getDetailedExplanation()}
          </p>
        </CardContent>
      </Card>

      {/* Visual Color Harmony Indicator */}
      <div className="flex justify-center">
        <div className="flex items-center space-x-3">
          <div className="text-sm font-medium text-muted-foreground font-[Inter]">
            Color Harmony:
          </div>
          <div className={`px-4 py-2 rounded-full text-sm font-semibold transition-colors ${
            color.verdict === 'best'
              ? 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300'
              : 'bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-300'
          }`}>
            {color.verdict === 'best' ? 'Excellent' : 'Poor'}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ColorDetails;