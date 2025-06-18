"""
Professional Face Shape Recommendations System
Provides detailed beauty recommendations based on face shape analysis.
"""

from typing import Dict, List, Any

class FaceShapeRecommendations:
    """
    Professional recommendations system for different face shapes.
    Based on beauty industry standards and expert advice.
    """
    
    def __init__(self):
        """Initialize the recommendations database."""
        self.recommendations = {
            "Oval": {
                "description": "Oval faces are considered the ideal face shape with balanced proportions. You have versatile features that work well with most styles.",
                "strengths": [
                    "Naturally balanced proportions",
                    "Versatile for most hairstyles and makeup looks",
                    "Well-defined cheekbones",
                    "Harmonious facial features"
                ],
                "hairstyles": {
                    "recommended": [
                        "Almost any hairstyle works well",
                        "Long layers to enhance natural balance",
                        "Side-swept bangs",
                        "Bob cuts at any length",
                        "Pixie cuts for bold looks",
                        "Updos and ponytails"
                    ],
                    "avoid": [
                        "Styles that completely hide your face shape",
                        "Extremely heavy, blunt bangs that cover the forehead entirely"
                    ]
                },
                "makeup": {
                    "contouring": "Minimal contouring needed. Light highlighting on cheekbones and bridge of nose.",
                    "eyebrows": "Follow your natural brow shape. Soft arches work beautifully.",
                    "eyes": "Any eye makeup style works. Experiment with different looks.",
                    "lips": "All lip shapes and colors are flattering."
                },
                "accessories": {
                    "earrings": "All styles work - studs, hoops, dangles, chandeliers",
                    "glasses": "Most frame shapes are flattering",
                    "hats": "Wide variety of hat styles suit oval faces"
                }
            },
            
            "Round": {
                "description": "Round faces have soft, curved lines with similar width and length. The goal is to add definition and create the illusion of length.",
                "strengths": [
                    "Youthful, soft appearance",
                    "Smooth, curved jawline",
                    "Full cheeks that can be beautifully highlighted",
                    "Naturally feminine features"
                ],
                "hairstyles": {
                    "recommended": [
                        "Long layers that fall below the chin",
                        "Side parts to create asymmetry",
                        "Voluminous styles on top",
                        "Long, straight hair",
                        "Angled bobs (longer in front)",
                        "High ponytails and updos"
                    ],
                    "avoid": [
                        "Blunt, chin-length bobs",
                        "Center parts",
                        "Styles that add width at the sides",
                        "Very short, cropped styles",
                        "Curls that add volume at the sides"
                    ]
                },
                "makeup": {
                    "contouring": "Contour along the sides of the face and under the jawline. Highlight the center of the face vertically.",
                    "eyebrows": "Create height with arched brows to elongate the face.",
                    "eyes": "Elongated eye makeup. Wing eyeliner upward and outward.",
                    "lips": "Slightly overlining the lips can add definition."
                },
                "accessories": {
                    "earrings": "Long, dangly earrings to create vertical lines",
                    "glasses": "Rectangular or angular frames",
                    "hats": "Avoid wide-brimmed hats; choose styles with height"
                }
            },
            
            "Square": {
                "description": "Square faces have strong, angular features with a broad forehead and jawline. The goal is to soften angles and add curves.",
                "strengths": [
                    "Strong, defined jawline",
                    "Striking, powerful appearance",
                    "Well-defined facial structure",
                    "Naturally bold features"
                ],
                "hairstyles": {
                    "recommended": [
                        "Soft, layered cuts",
                        "Side-swept bangs",
                        "Waves and curls to soften angles",
                        "Long hair with soft layers",
                        "Asymmetrical styles",
                        "Rounded bob cuts"
                    ],
                    "avoid": [
                        "Blunt, straight-across bangs",
                        "Very short, geometric cuts",
                        "Styles that emphasize the jawline",
                        "Center parts with straight hair",
                        "Slicked-back styles"
                    ]
                },
                "makeup": {
                    "contouring": "Soften the jawline with contouring. Round out the forehead corners.",
                    "eyebrows": "Soft, rounded brow shapes rather than angular",
                    "eyes": "Rounded eye makeup shapes. Avoid harsh, angular lines.",
                    "lips": "Rounded lip shapes. Avoid overly defined, angular lip lines."
                },
                "accessories": {
                    "earrings": "Rounded hoops, curved designs, avoid geometric shapes",
                    "glasses": "Round or oval frames to soften angular features",
                    "hats": "Soft, rounded hat styles"
                }
            },
            
            "Heart": {
                "description": "Heart-shaped faces have a wider forehead and narrower chin. The goal is to balance the upper and lower portions of the face.",
                "strengths": [
                    "Striking, memorable features",
                    "Beautiful, prominent cheekbones",
                    "Delicate, pointed chin",
                    "Naturally photogenic angles"
                ],
                "hairstyles": {
                    "recommended": [
                        "Chin-length bobs to add width at the jawline",
                        "Side-swept bangs to minimize forehead width",
                        "Layers that start at the chin",
                        "Styles that add volume at the bottom",
                        "Wispy, textured bangs",
                        "Hair tucked behind ears to show jawline"
                    ],
                    "avoid": [
                        "Very short styles that emphasize the forehead",
                        "Slicked-back styles",
                        "Heavy, full bangs",
                        "Styles that add volume on top",
                        "Center parts with no bangs"
                    ]
                },
                "makeup": {
                    "contouring": "Minimize forehead width, add definition to the chin area.",
                    "eyebrows": "Keep brows proportional, not too thick or thin",
                    "eyes": "Balance is key - don't overemphasize the upper portion",
                    "lips": "Fuller lip looks can help balance the narrow chin."
                },
                "accessories": {
                    "earrings": "Wider styles at the bottom, teardrops, triangular shapes",
                    "glasses": "Bottom-heavy frames or cat-eye styles",
                    "hats": "Styles that don't add width to the forehead"
                }
            },
            
            "Diamond": {
                "description": "Diamond faces have narrow foreheads and jawlines with wider cheekbones. The goal is to balance the proportions.",
                "strengths": [
                    "Striking, defined cheekbones",
                    "Unique, memorable face shape",
                    "Naturally sculpted appearance",
                    "Beautiful bone structure"
                ],
                "hairstyles": {
                    "recommended": [
                        "Styles that add width to forehead and chin",
                        "Side-swept bangs",
                        "Chin-length layers",
                        "Textured, voluminous styles",
                        "Deep side parts",
                        "Styles that frame the face softly"
                    ],
                    "avoid": [
                        "Styles that emphasize cheekbone width",
                        "Very short, cropped styles",
                        "Slicked-back looks",
                        "Styles pulled tight at the temples",
                        "Center parts"
                    ]
                },
                "makeup": {
                    "contouring": "Add width to forehead and chin, minimize cheekbone prominence",
                    "eyebrows": "Fuller brows to add width to the forehead area",
                    "eyes": "Horizontal eye makeup to add width",
                    "lips": "Fuller lips to balance narrow chin"
                },
                "accessories": {
                    "earrings": "Studs or small hoops that don't emphasize width",
                    "glasses": "Frames that add width to forehead and chin areas",
                    "hats": "Styles that add width to the forehead"
                }
            },
            
            "Oblong": {
                "description": "Oblong faces are longer than they are wide. The goal is to create the illusion of width and minimize length.",
                "strengths": [
                    "Elegant, sophisticated appearance",
                    "Naturally refined features",
                    "Photogenic profile",
                    "Graceful proportions"
                ],
                "hairstyles": {
                    "recommended": [
                        "Blunt bangs to shorten the forehead",
                        "Layered cuts that add width",
                        "Bob cuts at chin or shoulder length",
                        "Waves and curls for added volume",
                        "Side parts with volume",
                        "Styles that add width at the sides"
                    ],
                    "avoid": [
                        "Very long, straight hair",
                        "High ponytails and updos",
                        "Styles that add height on top",
                        "Center parts with no bangs",
                        "Sleek, flat styles"
                    ]
                },
                "makeup": {
                    "contouring": "Add width with horizontal contouring techniques",
                    "eyebrows": "Horizontal, straight brows rather than high arches",
                    "eyes": "Horizontal eye makeup, avoid too much vertical emphasis",
                    "lips": "Wider lip shapes to add horizontal emphasis"
                },
                "accessories": {
                    "earrings": "Wide hoops, button earrings, horizontal designs",
                    "glasses": "Wide frames that add horizontal emphasis",
                    "hats": "Wide-brimmed styles"
                }
            },
            
            "Triangle": {
                "description": "Triangle faces have a narrow forehead and wider jawline. The goal is to balance by adding width to the upper face.",
                "strengths": [
                    "Strong, defined jawline",
                    "Unique, striking appearance",
                    "Naturally bold features",
                    "Distinctive bone structure"
                ],
                "hairstyles": {
                    "recommended": [
                        "Styles that add volume on top",
                        "Side-swept bangs",
                        "Layered cuts with volume at the crown",
                        "Asymmetrical styles",
                        "Textured, voluminous styles",
                        "Styles that widen the forehead area"
                    ],
                    "avoid": [
                        "Styles that add width at the jawline",
                        "Very short styles",
                        "Slicked-back looks",
                        "Styles that emphasize the jaw",
                        "Heavy, straight bangs"
                    ]
                },
                "makeup": {
                    "contouring": "Add width to forehead, minimize jawline width",
                    "eyebrows": "Fuller, more prominent brows to balance the face",
                    "eyes": "Emphasize the upper portion of the face",
                    "lips": "Keep lip emphasis moderate to not compete with the jawline"
                },
                "accessories": {
                    "earrings": "Styles that add width to the upper face",
                    "glasses": "Top-heavy frames or cat-eye styles",
                    "hats": "Styles that add width to the forehead area"
                }
            }
        }
    
    def get_recommendations(self, face_shape: str) -> Dict[str, Any]:
        """
        Get comprehensive recommendations for a specific face shape.
        
        Args:
            face_shape: The detected face shape
            
        Returns:
            Dictionary containing detailed recommendations
        """
        return self.recommendations.get(face_shape, self.recommendations["Oval"])
    
    def get_quick_tips(self, face_shape: str) -> List[str]:
        """
        Get quick styling tips for a face shape.
        
        Args:
            face_shape: The detected face shape
            
        Returns:
            List of quick styling tips
        """
        recommendations = self.get_recommendations(face_shape)
        
        quick_tips = []
        quick_tips.append(f"Your {face_shape.lower()} face shape: {recommendations['description']}")
        
        # Add top hairstyle recommendations
        if recommendations['hairstyles']['recommended']:
            quick_tips.append(f"Best hairstyles: {', '.join(recommendations['hairstyles']['recommended'][:3])}")
        
        # Add key makeup tip
        if 'contouring' in recommendations['makeup']:
            quick_tips.append(f"Makeup tip: {recommendations['makeup']['contouring']}")
        
        return quick_tips
