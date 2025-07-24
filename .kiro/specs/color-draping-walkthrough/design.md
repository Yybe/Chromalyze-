# Design Document

## Overview

The Color Draping Walkthrough creates an immersive digital recreation of a professional color draping session. Users see their uploaded photo with realistic fabric swatches positioned under their chin, accompanied by AI feedback about each color's impact. The experience transforms static analysis results into an engaging, educational journey that builds confidence in personal color choices.

## Architecture

### Component Hierarchy

```
ColorDrapingWalkthrough/
├── EntryScreen
│   ├── WelcomeMessage ("Your Color Analysis is Ready!")
│   ├── ViewSummaryButton
│   └── StartWalkthroughButton
├── WalkthroughFlow
│   ├── PhotoWithFabric
│   │   ├── UserPhoto (static, top half)
│   │   └── FabricSwatch (realistic overlay under chin)
│   ├── ColorDetails
│   │   ├── VerdictBadge (✅/❌)
│   │   ├── ColorName
│   │   └── AIFeedback
│   └── Navigation
│       ├── BackButton
│       ├── NextButton
│       └── ProgressIndicator
└── SummaryScreen
    ├── ColorSeasonHeader
    ├── TopColorsGrid (5 best)
    ├── FullPaletteGrid
    ├── AvoidColorsSection
    └── ActionButtons
        ├── DownloadButton
        ├── ShareButton
        └── RestartButton
```

### Data Flow

1. **Entry**: User chooses walkthrough from completed analysis
2. **Transform**: Convert existing analysis to walkthrough format
3. **Navigate**: Step through each color with fabric simulation
4. **Summarize**: Present consolidated results with actions

## Components and Interfaces

### Data Models

```typescript
interface WalkthroughData {
  userPhoto: string;
  colorSeason: string;
  colors: ColorItem[];
  analysisId: string;
}

interface ColorItem {
  name: string;
  hex: string;
  verdict: 'best' | 'avoid';
  feedback: string;
}

interface FabricProps {
  color: string;
  isAnimating: boolean;
  fabricType: 'silk' | 'cotton' | 'wool';
}
```

### EntryScreen

**Purpose**: Present viewing options after analysis completion

**Layout**:
- Centered welcome message with elegant typography
- Two prominent buttons with clear visual hierarchy:
  - [View Full Analysis] → Navigate to existing enhanced results page
  - [Walk Through Your Palette →] → Start walkthrough experience
- Smooth transition animations to chosen path

**Styling**:
- Luxury color palette (warm golds, soft creams)
- Large, readable typography
- Subtle background textures

### PhotoWithFabric

**Purpose**: Core draping simulation component

**Photo Display**:
- Responsive image in top 60% of screen
- Maintains aspect ratio across devices
- Subtle frame for professional appearance

**Fabric Swatch**:
- Positioned under chin area (bottom 20% of photo)
- 60% width, centered horizontally
- Realistic textures using CSS gradients
- Soft drop shadows for depth

**CSS Implementation**:
```css
.fabric-swatch {
  position: absolute;
  bottom: 20%;
  left: 50%;
  transform: translateX(-50%);
  width: 60%;
  height: 25%;
  border-radius: 8px 8px 0 0;
  box-shadow: 0 6px 20px rgba(0,0,0,0.3);
  background: linear-gradient(145deg, 
    var(--color), 
    color-mix(in srgb, var(--color) 80%, black)
  );
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.fabric-swatch::before {
  content: '';
  position: absolute;
  inset: 0;
  background: 
    radial-gradient(circle at 30% 30%, rgba(255,255,255,0.3) 1px, transparent 1px),
    radial-gradient(circle at 70% 70%, rgba(0,0,0,0.1) 1px, transparent 1px);
  background-size: 4px 4px, 6px 6px;
  border-radius: inherit;
}
```

### ColorDetails

**Purpose**: Display color information and feedback

**Verdict Badge**:
- Top-right corner positioning
- ✅ for best colors (green background)
- ❌ for avoid colors (red background)
- Rounded corners with subtle shadow

**Color Name**:
- Large, bold typography (2rem)
- Centered below photo
- High contrast for readability

**AI Feedback**:
- Conversational, encouraging tone
- Proper line height for readability
- Fade-in animation on color change

### Navigation

**Purpose**: Intuitive walkthrough controls

**Button Design**:
- Large touch targets (44px minimum)
- Rounded corners with subtle gradients
- Disabled state styling for boundaries
- Smooth hover/press animations

**Progress Indicator**:
- "3 of 12" format
- Small, unobtrusive positioning
- Smooth progress bar animation

**Swipe Support**:
- Touch gesture recognition
- Visual feedback during swipe
- Proper threshold handling

### SummaryScreen

**Purpose**: Comprehensive results presentation

**Color Season Header**:
- Large, celebratory typography
- Prominent positioning at top
- Subtle background accent

**Top Colors Grid**:
- 5 best colors in prominent display
- Color swatches with names
- Brief feedback for each

**Full Palette Grid**:
- Organized by color categories
- Consistent swatch sizing
- Hover effects for interaction

**Avoid Colors Section**:
- Visually separated with gray background
- Reduced opacity for distinction
- Clear reasoning for each color

## Error Handling

### Image Loading
- Skeleton placeholder during load
- Fallback image if photo fails
- Retry mechanism with user feedback
- Graceful degradation to text-only

### Data Validation
- Check for required color properties
- Fallback feedback messages
- Default verdict assignment
- Empty state handling

### Navigation Edge Cases
- Boundary checking for first/last colors
- State recovery on page refresh
- Proper cleanup on component unmount

## Testing Strategy

### Visual Testing
- Screenshot comparisons for each color
- Cross-browser fabric rendering
- Mobile responsiveness validation
- Animation smoothness verification

### Interaction Testing
- Button navigation functionality
- Swipe gesture recognition
- Keyboard accessibility
- Touch target sizing

### Integration Testing
- Data transformation accuracy
- State persistence during navigation
- Proper cleanup and memory management

## Performance Considerations

### Image Optimization
- Lazy loading for large photos
- WebP format with fallbacks
- Responsive image sizing
- Caching strategies

### Animation Performance
- CSS transforms over layout changes
- Hardware acceleration utilization
- Reduced motion support
- Frame rate monitoring

### Bundle Optimization
- Code splitting for walkthrough
- Tree shaking unused components
- Compressed texture assets
- Efficient re-rendering patterns

## Accessibility

### Screen Reader Support
- Semantic HTML structure
- ARIA labels for dynamic content
- Live regions for color changes
- Descriptive alt text

### Keyboard Navigation
- Tab order management
- Arrow key support for navigation
- Enter/Space for button activation
- Focus indicators

### Visual Accessibility
- WCAG AA color contrast compliance
- Reduced motion preferences
- High contrast mode support
- Scalable text sizing

## Integration Points

### Data Source
- Transform existing ComprehensiveAnalysisResult from analysis service
- Extract color data from recommendations.colors (primary, secondary, neutrals, avoid)
- Use colorSeason.season for season display
- Generate feedback messages for each color based on analysis

### Navigation Flow
- Entry point: After analysis completion, before showing results
- [View Full Analysis] → Navigate to existing enhanced results page (/analyze/[id])
- [Walk Through Your Palette] → Start walkthrough experience (/analyze/[id]/walkthrough)
- From summary screen → Option to view full analysis
- Proper URL routing and browser history management

### Styling Consistency
- Use existing design tokens
- Match current brand aesthetic
- Consistent component patterns
- Responsive breakpoints alignment