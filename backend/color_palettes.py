# Standard 12-Season Color Palettes
# Based on common color theory interpretations. Hex codes are approximate representations.

COLOR_PALETTES = {
    # SPRING
    "Light Spring": {
        "description": "Light, warm, and bright. Think delicate spring blossoms.",
        "recommended": [
            {"name": "Light Peach", "hex": "#FFDAB9"},
            {"name": "Soft Yellow", "hex": "#FFFACD"},
            {"name": "Mint Green", "hex": "#98FB98"},
            {"name": "Aqua Blue", "hex": "#AFEEEE"},
            {"name": "Coral Pink", "hex": "#FF7F50"},
            {"name": "Light Gold", "hex": "#EEE8AA"},
            {"name": "Powder Blue", "hex": "#B0E0E6"},
            {"name": "Ivory", "hex": "#FFFFF0"},
        ],
        "avoid": [
            {"name": "Black", "hex": "#000000"},
            {"name": "Dark Burgundy", "hex": "#800020"},
            {"name": "Olive Green", "hex": "#808000"},
            {"name": "Mustard Yellow", "hex": "#FFDB58"},
            {"name": "Deep Teal", "hex": "#008080"},
        ],
    },
    "Warm Spring": {
        "description": "Warm, clear, and vibrant. Think tropical flowers and sunshine.",
        "recommended": [
            {"name": "Warm Coral", "hex": "#FF7F50"},
            {"name": "Golden Yellow", "hex": "#FFDA57"},
            {"name": "Lime Green", "hex": "#32CD32"},
            {"name": "Turquoise", "hex": "#40E0D0"},
            {"name": "Creamy White", "hex": "#FFFDD0"},
            {"name": "Tomato Red", "hex": "#FF6347"},
            {"name": "Bright Navy", "hex": "#0000CD"},
            {"name": "Peach", "hex": "#FFDAB9"},
        ],
        "avoid": [
            {"name": "Cool Gray", "hex": "#808080"},
            {"name": "Dusty Rose", "hex": "#D8BFD8"},
            {"name": "Icy Blue", "hex": "#ADD8E6"},
            {"name": "Black", "hex": "#000000"},
            {"name": "Silver", "hex": "#C0C0C0"},
        ],
    },
    "Clear Spring": {
        "description": "Clear, bright, warm, and high contrast. Think vivid, clear colors.",
        "recommended": [
            {"name": "Bright Red", "hex": "#FF0000"},
            {"name": "Emerald Green", "hex": "#2E8B57"},
            {"name": "Royal Blue", "hex": "#4169E1"},
            {"name": "Hot Pink", "hex": "#FF69B4"},
            {"name": "True Yellow", "hex": "#FFFF00"},
            {"name": "Black", "hex": "#000000"}, # High contrast works
            {"name": "Pure White", "hex": "#FFFFFF"},
            {"name": "Bright Coral", "hex": "#FF7F50"},
        ],
        "avoid": [
            {"name": "Muted Mauve", "hex": "#E0B0FF"},
            {"name": "Dusty Brown", "hex": "#A0522D"},
            {"name": "Olive Green", "hex": "#808000"},
            {"name": "Beige", "hex": "#F5F5DC"},
            {"name": "Grayish Blue", "hex": "#A2A2D0"},
        ],
    },
    # SUMMER
    "Light Summer": {
        "description": "Light, cool, and soft. Think hazy summer skies and delicate florals.",
        "recommended": [
            {"name": "Powder Blue", "hex": "#B0E0E6"},
            {"name": "Soft Pink", "hex": "#FFB6C1"},
            {"name": "Lavender", "hex": "#E6E6FA"},
            {"name": "Light Gray", "hex": "#D3D3D3"},
            {"name": "Mint Green", "hex": "#98FB98"},
            {"name": "Rose Beige", "hex": "#F5F5DC"}, # Adjusted
            {"name": "Sky Blue", "hex": "#87CEEB"},
            {"name": "Soft White", "hex": "#F8F8FF"},
        ],
        "avoid": [
            {"name": "Black", "hex": "#000000"},
            {"name": "Bright Orange", "hex": "#FFA500"},
            {"name": "Golden Yellow", "hex": "#FFDA57"},
            {"name": "Olive Green", "hex": "#808000"},
            {"name": "Mustard", "hex": "#FFDB58"},
        ],
    },
    "Cool Summer": {
        "description": "Cool, muted, and elegant. Think deep ocean blues and rose gardens.",
        "recommended": [
            {"name": "Cool Blue", "hex": "#4682B4"},
            {"name": "Rose Pink", "hex": "#FF66CC"},
            {"name": "Gray Blue", "hex": "#6A5ACD"}, # SlateBlue
            {"name": "Soft Fuchsia", "hex": "#C71585"}, # MediumVioletRed
            {"name": "Emerald Green (cool)", "hex": "#009B77"},
            {"name": "Charcoal Gray", "hex": "#36454F"},
            {"name": "Burgundy (cool)", "hex": "#800020"},
            {"name": "Silver Gray", "hex": "#C0C0C0"},
        ],
        "avoid": [
            {"name": "Orange", "hex": "#FFA500"},
            {"name": "Golden Yellow", "hex": "#FFDA57"},
            {"name": "Warm Brown", "hex": "#A0522D"},
            {"name": "Olive Green", "hex": "#808000"},
            {"name": "Peach", "hex": "#FFDAB9"},
        ],
    },
    "Soft Summer": {
        "description": "Soft, muted, cool with a neutral lean. Think misty landscapes.",
        "recommended": [
            {"name": "Dusty Rose", "hex": "#D8BFD8"},
            {"name": "Jade Green", "hex": "#00A86B"},
            {"name": "Gray-Blue", "hex": "#A2A2D0"}, # Adjusted
            {"name": "Soft Teal", "hex": "#4682B4"}, # SteelBlue
            {"name": "Rose Brown", "hex": "#BC8F8F"},
            {"name": "Stone Gray", "hex": "#778899"}, # LightSlateGray
            {"name": "Muted Plum", "hex": "#DDA0DD"},
            {"name": "Off-White", "hex": "#FAF0E6"}, # Linen
        ],
        "avoid": [
            {"name": "Bright Yellow", "hex": "#FFFF00"},
            {"name": "Electric Blue", "hex": "#7DF9FF"},
            {"name": "Pure Black", "hex": "#000000"},
            {"name": "Bright Orange", "hex": "#FFA500"},
            {"name": "Hot Pink", "hex": "#FF69B4"},
        ],
    },
    # AUTUMN
    "Soft Autumn": {
        "description": "Soft, muted, warm with a neutral lean. Think gentle autumn fields.",
        "recommended": [
            {"name": "Olive Green", "hex": "#808000"},
            {"name": "Muted Gold", "hex": "#B08D57"}, # Adjusted
            {"name": "Salmon Pink", "hex": "#FA8072"},
            {"name": "Warm Beige", "hex": "#F5F5DC"},
            {"name": "Mahogany", "hex": "#C04000"},
            {"name": "Butter Yellow", "hex": "#FFFACD"}, # LemonChiffon
            {"name": "Soft Teal (warm)", "hex": "#008080"},
            {"name": "Cream", "hex": "#FFFDD0"},
        ],
        "avoid": [
            {"name": "Bright Fuchsia", "hex": "#FF00FF"},
            {"name": "Icy Blue", "hex": "#ADD8E6"},
            {"name": "Pure Black", "hex": "#000000"},
            {"name": "Silver", "hex": "#C0C0C0"},
            {"name": "Cool Gray", "hex": "#808080"},
        ],
    },
    "Warm Autumn": {
        "description": "Warm, rich, and earthy. Think autumn leaves and spices.",
        "recommended": [
            {"name": "Terracotta", "hex": "#E2725B"},
            {"name": "Mustard Yellow", "hex": "#FFDB58"},
            {"name": "Olive Green", "hex": "#808000"},
            {"name": "Deep Peach", "hex": "#FFCBA4"},
            {"name": "Chocolate Brown", "hex": "#D2691E"},
            {"name": "Forest Green", "hex": "#228B22"},
            {"name": "Burnt Orange", "hex": "#CC5500"},
            {"name": "Gold", "hex": "#FFD700"},
        ],
        "avoid": [
            {"name": "Cool Pink", "hex": "#FFC0CB"},
            {"name": "Silver", "hex": "#C0C0C0"},
            {"name": "Icy Blue", "hex": "#ADD8E6"},
            {"name": "Black", "hex": "#000000"},
            {"name": "Pure White", "hex": "#FFFFFF"},
        ],
    },
    "Deep Autumn": {
        "description": "Deep, warm, and rich. Think dark woods and embers.",
        "recommended": [
            {"name": "Deep Olive", "hex": "#556B2F"},
            {"name": "Chocolate Brown", "hex": "#7B3F00"},
            {"name": "Burnt Orange", "hex": "#CC5500"},
            {"name": "Mustard Yellow", "hex": "#FFDB58"},
            {"name": "Forest Green", "hex": "#228B22"},
            {"name": "Deep Teal (warm)", "hex": "#008080"},
            {"name": "Burgundy (warm)", "hex": "#8B0000"}, # DarkRed
            {"name": "Cream", "hex": "#FFFDD0"},
        ],
        "avoid": [
            {"name": "Pastel Pink", "hex": "#FFD1DC"},
            {"name": "Icy Blue", "hex": "#ADD8E6"},
            {"name": "Silver", "hex": "#C0C0C0"},
            {"name": "Bright Fuchsia", "hex": "#FF00FF"},
            {"name": "Pure White", "hex": "#FFFFFF"},
        ],
    },
    # WINTER
    "Deep Winter": {
        "description": "Deep, cool, and clear. Think rich jewel tones and stark contrasts.",
        "recommended": [
            {"name": "Black", "hex": "#000000"},
            {"name": "Pure White", "hex": "#FFFFFF"},
            {"name": "Ruby Red", "hex": "#E0115F"},
            {"name": "Emerald Green", "hex": "#50C878"},
            {"name": "Sapphire Blue", "hex": "#0F52BA"},
            {"name": "Deep Fuchsia", "hex": "#C154C1"},
            {"name": "Charcoal Gray", "hex": "#36454F"},
            {"name": "Icy Blue", "hex": "#ADD8E6"},
        ],
        "avoid": [
            {"name": "Orange", "hex": "#FFA500"},
            {"name": "Golden Yellow", "hex": "#FFDA57"},
            {"name": "Olive Green", "hex": "#808000"},
            {"name": "Beige", "hex": "#F5F5DC"},
            {"name": "Warm Brown", "hex": "#A0522D"},
        ],
    },
    "Cool Winter": {
        "description": "Cool, intense, and sharp. Think icy landscapes and bold contrasts.",
        "recommended": [
            {"name": "True Blue", "hex": "#0000FF"},
            {"name": "Icy Pink", "hex": "#FFB6C1"}, # LightPink
            {"name": "Deep Purple", "hex": "#800080"},
            {"name": "Silver", "hex": "#C0C0C0"},
            {"name": "Black", "hex": "#000000"},
            {"name": "Pure White", "hex": "#FFFFFF"},
            {"name": "Cool Red (Blue-based)", "hex": "#C71585"}, # MediumVioletRed as proxy
            {"name": "Charcoal Gray", "hex": "#36454F"},
        ],
        "avoid": [
            {"name": "Orange", "hex": "#FFA500"},
            {"name": "Gold", "hex": "#FFD700"},
            {"name": "Mustard Yellow", "hex": "#FFDB58"},
            {"name": "Olive Green", "hex": "#808000"},
            {"name": "Warm Brown", "hex": "#A0522D"},
        ],
    },
    "Clear Winter": {
        "description": "Clear, bright, cool, and high contrast. Think primary colors and sharp clarity.",
        "recommended": [
            {"name": "True Red", "hex": "#FF0000"},
            {"name": "Royal Blue", "hex": "#4169E1"},
            {"name": "Emerald Green", "hex": "#2E8B57"},
            {"name": "Hot Pink", "hex": "#FF69B4"},
            {"name": "Black", "hex": "#000000"},
            {"name": "Pure White", "hex": "#FFFFFF"},
            {"name": "Icy Yellow", "hex": "#FFFACD"}, # LemonChiffon
            {"name": "Bright Purple", "hex": "#BF00FF"}, # Electric Purple
        ],
        "avoid": [
            {"name": "Dusty Rose", "hex": "#D8BFD8"},
            {"name": "Olive Green", "hex": "#808000"},
            {"name": "Beige", "hex": "#F5F5DC"},
            {"name": "Muted Gold", "hex": "#B08D57"},
            {"name": "Warm Brown", "hex": "#A0522D"},
        ],
    },
}

# Function to get palette data
def get_palette(season_name):
    """Returns the palette dictionary for a given season name, or None if not found."""
    return COLOR_PALETTES.get(season_name)
