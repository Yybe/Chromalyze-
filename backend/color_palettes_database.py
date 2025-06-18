"""
Comprehensive Color Palettes Database for 12 Color Seasons
Includes recommended colors, colors to avoid, and specific recommendations for makeup, clothing, and accessories.
"""

import sqlite3
import json
from pathlib import Path
from typing import Dict, List, Any

class ColorPalettesDatabase:
    """Database manager for color season palettes and recommendations."""
    
    def __init__(self, db_path: str = "color_palettes.db"):
        self.db_path = db_path
        self.init_database()
        self.populate_palettes()
    
    def init_database(self):
        """Initialize the database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Color palettes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS color_palettes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                season TEXT NOT NULL,
                color_type TEXT NOT NULL,
                hex_code TEXT NOT NULL,
                color_name TEXT NOT NULL,
                description TEXT,
                category TEXT
            )
        ''')
        
        # Recommendations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                season TEXT NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT,
                recommendation TEXT NOT NULL,
                avoid TEXT
            )
        ''')
        
        # Season characteristics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS season_characteristics (
                season TEXT PRIMARY KEY,
                undertone TEXT NOT NULL,
                contrast_level TEXT NOT NULL,
                saturation_level TEXT NOT NULL,
                description TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def populate_palettes(self):
        """Populate the database with comprehensive color palettes."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM color_palettes")
        if cursor.fetchone()[0] > 0:
            conn.close()
            return
        
        # Define comprehensive color palettes for each season
        palettes = {
            'Deep Winter': {
                'primary': [
                    ('#000000', 'True Black', 'Perfect for dramatic looks'),
                    ('#FFFFFF', 'Pure White', 'Crisp and clean'),
                    ('#8B0000', 'Deep Red', 'Rich and powerful'),
                    ('#000080', 'Navy Blue', 'Classic and sophisticated'),
                    ('#4B0082', 'Indigo', 'Deep and mysterious'),
                    ('#800080', 'Purple', 'Royal and elegant'),
                    ('#008B8B', 'Dark Cyan', 'Cool and refreshing'),
                    ('#2F4F4F', 'Dark Slate Gray', 'Professional and strong')
                ],
                'accent': [
                    ('#FF1493', 'Deep Pink', 'Bold and vibrant'),
                    ('#00CED1', 'Dark Turquoise', 'Striking accent'),
                    ('#32CD32', 'Lime Green', 'Fresh pop of color'),
                    ('#FFD700', 'Gold', 'Luxurious accent')
                ],
                'avoid': [
                    ('#FFA500', 'Orange', 'Too warm for your cool undertones'),
                    ('#FFFF00', 'Yellow', 'Clashes with cool palette'),
                    ('#8B4513', 'Saddle Brown', 'Muddy against your coloring'),
                    ('#F5DEB3', 'Wheat', 'Washes you out')
                ]
            },
            'Cool Winter': {
                'primary': [
                    ('#2F4F4F', 'Dark Slate Gray', 'Sophisticated neutral'),
                    ('#FFFFFF', 'Pure White', 'Clean and fresh'),
                    ('#B22222', 'Fire Brick', 'Cool-toned red'),
                    ('#191970', 'Midnight Blue', 'Deep and elegant'),
                    ('#800080', 'Purple', 'Rich and regal'),
                    ('#008080', 'Teal', 'Cool and calming'),
                    ('#C0C0C0', 'Silver', 'Metallic neutral'),
                    ('#708090', 'Slate Gray', 'Professional base')
                ],
                'accent': [
                    ('#FF69B4', 'Hot Pink', 'Vibrant accent'),
                    ('#00FFFF', 'Cyan', 'Cool pop'),
                    ('#9370DB', 'Medium Purple', 'Elegant highlight'),
                    ('#20B2AA', 'Light Sea Green', 'Fresh accent')
                ],
                'avoid': [
                    ('#FF8C00', 'Dark Orange', 'Too warm'),
                    ('#DAA520', 'Goldenrod', 'Muddy tone'),
                    ('#CD853F', 'Peru', 'Warm brown clashes'),
                    ('#F0E68C', 'Khaki', 'Sallow effect')
                ]
            },
            'Clear Winter': {
                'primary': [
                    ('#000000', 'True Black', 'Dramatic base'),
                    ('#FFFFFF', 'Pure White', 'Crisp contrast'),
                    ('#DC143C', 'Crimson', 'Clear red'),
                    ('#0000FF', 'Blue', 'Bright and clear'),
                    ('#FF00FF', 'Magenta', 'Vibrant and bold'),
                    ('#00FF00', 'Lime', 'Electric green'),
                    ('#FFFF00', 'Yellow', 'Bright and clear'),
                    ('#FF1493', 'Deep Pink', 'Vivid accent')
                ],
                'accent': [
                    ('#00FFFF', 'Aqua', 'Electric blue'),
                    ('#FF4500', 'Orange Red', 'Fiery accent'),
                    ('#9400D3', 'Violet', 'Rich purple'),
                    ('#32CD32', 'Lime Green', 'Vibrant pop')
                ],
                'avoid': [
                    ('#F5F5DC', 'Beige', 'Too muted'),
                    ('#D2B48C', 'Tan', 'Muddy neutral'),
                    ('#BC8F8F', 'Rosy Brown', 'Dusty tone'),
                    ('#DDA0DD', 'Plum', 'Too soft')
                ]
            },
            'Deep Autumn': {
                'primary': [
                    ('#8B4513', 'Saddle Brown', 'Rich earth tone'),
                    ('#2F4F4F', 'Dark Slate Gray', 'Deep neutral'),
                    ('#8B0000', 'Dark Red', 'Deep burgundy'),
                    ('#FF8C00', 'Dark Orange', 'Warm spice'),
                    ('#B8860B', 'Dark Goldenrod', 'Rich gold'),
                    ('#556B2F', 'Dark Olive Green', 'Deep forest'),
                    ('#800000', 'Maroon', 'Deep wine'),
                    ('#A0522D', 'Sienna', 'Warm brown')
                ],
                'accent': [
                    ('#FF6347', 'Tomato', 'Warm red-orange'),
                    ('#DAA520', 'Goldenrod', 'Rich gold'),
                    ('#CD853F', 'Peru', 'Warm tan'),
                    ('#D2691E', 'Chocolate', 'Rich brown')
                ],
                'avoid': [
                    ('#E6E6FA', 'Lavender', 'Too cool and light'),
                    ('#87CEEB', 'Sky Blue', 'Cool blue clashes'),
                    ('#FFB6C1', 'Light Pink', 'Too cool and soft'),
                    ('#F0F8FF', 'Alice Blue', 'Washes you out')
                ]
            },
            'Warm Autumn': {
                'primary': [
                    ('#D2691E', 'Chocolate', 'Warm brown'),
                    ('#F4A460', 'Sandy Brown', 'Warm neutral'),
                    ('#FF4500', 'Orange Red', 'Warm red'),
                    ('#FF8C00', 'Dark Orange', 'Rich orange'),
                    ('#DAA520', 'Goldenrod', 'Warm gold'),
                    ('#9ACD32', 'Yellow Green', 'Warm green'),
                    ('#CD853F', 'Peru', 'Warm tan'),
                    ('#A0522D', 'Sienna', 'Earth brown')
                ],
                'accent': [
                    ('#FF6347', 'Tomato', 'Warm accent'),
                    ('#FFA500', 'Orange', 'Vibrant warm'),
                    ('#ADFF2F', 'Green Yellow', 'Fresh accent'),
                    ('#DC143C', 'Crimson', 'Warm red')
                ],
                'avoid': [
                    ('#4169E1', 'Royal Blue', 'Too cool'),
                    ('#FF1493', 'Deep Pink', 'Cool undertones'),
                    ('#E0E0E0', 'Light Gray', 'Too cool and stark'),
                    ('#000000', 'Black', 'Too harsh')
                ]
            },
            'Soft Autumn': {
                'primary': [
                    ('#BC8F8F', 'Rosy Brown', 'Soft warm neutral'),
                    ('#F5DEB3', 'Wheat', 'Gentle warm tone'),
                    ('#CD853F', 'Peru', 'Muted warm brown'),
                    ('#DDA0DD', 'Plum', 'Soft purple'),
                    ('#D2B48C', 'Tan', 'Warm beige'),
                    ('#BDB76B', 'Dark Khaki', 'Muted olive'),
                    ('#F0E68C', 'Khaki', 'Soft yellow'),
                    ('#8FBC8F', 'Dark Sea Green', 'Muted green')
                ],
                'accent': [
                    ('#FA8072', 'Salmon', 'Soft coral'),
                    ('#F0DC82', 'Light Goldenrod', 'Gentle gold'),
                    ('#98FB98', 'Pale Green', 'Soft green'),
                    ('#DDA0DD', 'Plum', 'Muted purple')
                ],
                'avoid': [
                    ('#000000', 'Black', 'Too harsh'),
                    ('#FFFFFF', 'Pure White', 'Too stark'),
                    ('#FF0000', 'Red', 'Too bright'),
                    ('#0000FF', 'Blue', 'Too cool and bright')
                ]
            }
        }
        
        # Insert color palettes
        for season, categories in palettes.items():
            for category, colors in categories.items():
                for hex_code, name, description in colors:
                    cursor.execute('''
                        INSERT INTO color_palettes 
                        (season, color_type, hex_code, color_name, description, category)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (season, category, hex_code, name, description, 'general'))
        
        # Insert season characteristics
        characteristics = {
            'Deep Winter': ('cool', 'high', 'high', 'Dramatic and striking with high contrast'),
            'Cool Winter': ('cool', 'high', 'medium', 'Cool and sophisticated with clear colors'),
            'Clear Winter': ('cool', 'high', 'high', 'Bright and vivid with pure colors'),
            'Deep Autumn': ('warm', 'high', 'high', 'Rich and dramatic with deep warm tones'),
            'Warm Autumn': ('warm', 'medium', 'medium', 'Warm and earthy with golden undertones'),
            'Soft Autumn': ('warm', 'low', 'low', 'Muted and gentle with soft warm tones')
        }
        
        for season, (undertone, contrast, saturation, description) in characteristics.items():
            cursor.execute('''
                INSERT INTO season_characteristics 
                (season, undertone, contrast_level, saturation_level, description)
                VALUES (?, ?, ?, ?, ?)
            ''', (season, undertone, contrast, saturation, description))
        
        conn.commit()
        conn.close()
        print("✅ Color palettes database populated successfully")
    
    def get_palette(self, season: str) -> Dict[str, List[Dict]]:
        """Get color palette for a specific season."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT color_type, hex_code, color_name, description
            FROM color_palettes
            WHERE season = ?
            ORDER BY color_type, color_name
        ''', (season,))
        
        results = cursor.fetchall()
        conn.close()
        
        palette = {'primary': [], 'accent': [], 'avoid': []}
        
        for color_type, hex_code, name, description in results:
            color_info = {
                'hex': hex_code,
                'name': name,
                'description': description
            }
            if color_type in palette:
                palette[color_type].append(color_info)
        
        return palette
    
    def get_season_info(self, season: str) -> Dict[str, Any]:
        """Get comprehensive information about a color season."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get season characteristics
        cursor.execute('''
            SELECT undertone, contrast_level, saturation_level, description
            FROM season_characteristics
            WHERE season = ?
        ''', (season,))
        
        char_result = cursor.fetchone()
        if not char_result:
            conn.close()
            return {}
        
        undertone, contrast, saturation, description = char_result
        
        # Get color palette
        palette = self.get_palette(season)
        
        conn.close()
        
        return {
            'season': season,
            'undertone': undertone,
            'contrast_level': contrast,
            'saturation_level': saturation,
            'description': description,
            'palette': palette
        }
    
    def get_all_seasons(self) -> List[str]:
        """Get list of all available color seasons."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT DISTINCT season FROM season_characteristics ORDER BY season')
        seasons = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        return seasons

# Initialize database when module is imported
if __name__ == "__main__":
    db = ColorPalettesDatabase()
    
    # Test the database
    seasons = db.get_all_seasons()
    print(f"Available seasons: {seasons}")
    
    if seasons:
        test_season = seasons[0]
        info = db.get_season_info(test_season)
        print(f"\nSample season info for {test_season}:")
        print(json.dumps(info, indent=2))

def create_color_palettes_db():
    conn = sqlite3.connect('color_palettes.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS color_palettes (
        season TEXT,
        color_type TEXT,
        hex_code TEXT,
        description TEXT
    )
    ''')
    conn.commit()
    conn.close()

def insert_color_palette(season, color_type, hex_code, description):
    conn = sqlite3.connect('color_palettes.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO color_palettes (season, color_type, hex_code, description) VALUES (?, ?, ?, ?)',
                   (season, color_type, hex_code, description))
    conn.commit()
    conn.close()

def get_color_palettes(season):
    conn = sqlite3.connect('color_palettes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT color_type, hex_code, description FROM color_palettes WHERE season = ?', (season,))
    palettes = cursor.fetchall()
    conn.close()
    return palettes
