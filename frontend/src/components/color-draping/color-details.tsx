'use client';

import React from 'react';
import { DrapingColor } from '@/lib/color-draping-types';
import { Check, X } from 'lucide-react';

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
  const verdictClass = color.verdict === 'best' ? 'verdict-best' : 'verdict-avoid';

  return (
    <div className={`p-8 text-center transition-all duration-500 max-w-2xl mx-auto ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-5'} ${className}`}>
      {/* Verdict Badge */}
      <div className={`inline-flex items-center gap-2 px-6 py-3 rounded-full font-semibold text-sm uppercase tracking-wide mb-6 shadow-lg transition-all duration-300 ${
        color.verdict === 'best' 
          ? 'bg-gradient-to-r from-green-500 to-green-600 text-white' 
          : 'bg-gradient-to-r from-red-500 to-red-600 text-white'
      }`}>
        <VerdictIcon size={20} />
        <span>
          {color.verdict === 'best' ? 'Best' : 'Avoid'}
        </span>
      </div>

      {/* Color Name */}
      <h2 className="text-4xl font-bold text-gray-900 mb-4 leading-tight">
        {color.name}
      </h2>

      {/* Color Hex Display */}
      <div className="flex items-center justify-center gap-3 mb-8">
        <div 
          className="w-8 h-8 rounded-full border-2 border-white shadow-lg"
          style={{ backgroundColor: color.hex }}
        />
        <span className="font-mono text-sm text-gray-600 bg-gray-100 px-3 py-1 rounded font-medium">
          {color.hex}
        </span>
      </div>

      {/* AI Feedback */}
      <div className="mb-6">
        <p className="text-lg leading-relaxed text-gray-700 max-w-lg mx-auto italic">
          {color.feedback}
        </p>
      </div>

      {/* Category Badge (if available) */}
      {color.category && (
        <div className="inline-block">
          <span className="inline-block px-4 py-2 bg-gradient-to-r from-gray-100 to-gray-200 text-gray-600 rounded-full text-xs font-semibold uppercase tracking-wide border border-gray-300">
            {color.category.charAt(0).toUpperCase() + color.category.slice(1)} Color
          </span>
        </div>
      )}
    </div>
  );
};

export default ColorDetails;