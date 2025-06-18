import React from 'react';

const ColorSwatch = ({ hex, description }) => (
    <div className="flex flex-col items-center p-2 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow">
        <div className="w-20 h-20 rounded-full mb-2" style={{ backgroundColor: hex }}></div>
        <p className="text-sm text-gray-700 text-center">{description}</p>
    </div>
);

const RecommendationSection = ({ title, items }) => (
    <div className="mb-6">
        <h3 className="text-lg font-semibold mb-3 text-gray-800">{title}</h3>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {items.map((item, index) => (
                <div key={index} className="bg-white p-3 rounded-lg shadow-sm">
                    <p className="text-sm text-gray-700">{item}</p>
                </div>
            ))}
        </div>
    </div>
);

const ColorAnalysisResults = ({ season, palettes, faceShape }) => {
    // Group palettes by type
    const primaryColors = palettes.filter(p => p.color_type === 'primary');
    const accentColors = palettes.filter(p => p.color_type === 'accent');
    const neutralColors = palettes.filter(p => p.color_type === 'neutral');
    const avoidColors = palettes.filter(p => p.color_type === 'avoid');

    return (
        <div className="bg-white rounded-lg shadow-lg p-6">
            {/* Header Section */}
            <div className="text-center mb-8">
                <h2 className="text-3xl font-bold text-gray-800 mb-2">
                    Your Color Season: {season}
                </h2>
                <p className="text-gray-600">
                    Based on your natural coloring and undertones
                </p>
            </div>

            {/* Face Shape Section */}
            <div className="mb-8 p-4 bg-blue-50 rounded-lg">
                <h3 className="text-xl font-semibold text-gray-800 mb-2">
                    Your Face Shape: {faceShape}
                </h3>
                <p className="text-gray-600">
                    This shape complements your natural features and helps guide style recommendations
                </p>
            </div>

            {/* Color Palettes Section */}
            <div className="mb-8">
                <h3 className="text-xl font-semibold text-gray-800 mb-4">Your Color Palette</h3>
                
                {/* Primary Colors */}
                <div className="mb-6">
                    <h4 className="text-lg font-medium text-gray-700 mb-3">Primary Colors</h4>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        {primaryColors.map((color, index) => (
                            <ColorSwatch key={index} hex={color.hex_code} description={color.description} />
                        ))}
                    </div>
                </div>

                {/* Accent Colors */}
                <div className="mb-6">
                    <h4 className="text-lg font-medium text-gray-700 mb-3">Accent Colors</h4>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        {accentColors.map((color, index) => (
                            <ColorSwatch key={index} hex={color.hex_code} description={color.description} />
                        ))}
                    </div>
                </div>

                {/* Neutral Colors */}
                <div className="mb-6">
                    <h4 className="text-lg font-medium text-gray-700 mb-3">Neutral Colors</h4>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        {neutralColors.map((color, index) => (
                            <ColorSwatch key={index} hex={color.hex_code} description={color.description} />
                        ))}
                    </div>
                </div>

                {/* Colors to Avoid */}
                <div className="mb-6">
                    <h4 className="text-lg font-medium text-gray-700 mb-3">Colors to Avoid</h4>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        {avoidColors.map((color, index) => (
                            <ColorSwatch key={index} hex={color.hex_code} description={color.description} />
                        ))}
                    </div>
                </div>
            </div>

            {/* Recommendations Section */}
            <div className="mb-8">
                <h3 className="text-xl font-semibold text-gray-800 mb-4">Personalized Recommendations</h3>
                
                <RecommendationSection 
                    title="Makeup Recommendations"
                    items={[
                        "Opt for warm-toned foundations",
                        "Peachy blush shades",
                        "Terracotta lip colors",
                        "Golden eyeshadows"
                    ]}
                />

                <RecommendationSection 
                    title="Clothing Recommendations"
                    items={[
                        "Earthy tones for casual wear",
                        "Rich jewel tones for evening",
                        "Warm neutrals for business",
                        "Autumn-inspired patterns"
                    ]}
                />

                <RecommendationSection 
                    title="Accessory Recommendations"
                    items={[
                        "Gold jewelry",
                        "Warm-toned scarves",
                        "Leather accessories in warm browns",
                        "Copper and bronze accents"
                    ]}
                />
            </div>

            {/* Download Report Button */}
            <div className="text-center">
                <button className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors">
                    Download Full Analysis Report
                </button>
            </div>
        </div>
    );
};

export default ColorAnalysisResults; 