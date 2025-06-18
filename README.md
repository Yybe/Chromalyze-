# Chromalyze

Professional AI-powered beauty analysis platform that provides personalized face shape detection and color season analysis with tailored beauty recommendations.

## 🌟 Features

- **Face Shape Analysis**: Advanced geometric analysis using MediaPipe Face Mesh for accurate face shape classification
- **Color Season Analysis**: Lab color space analysis with 12-season classification system
- **Personalized Recommendations**: Tailored suggestions for hairstyles, makeup, colors, and accessories
- **Local Processing**: All analysis runs locally using WebAssembly for privacy and speed
- **Mobile-First Design**: Responsive interface optimized for all devices
- **Dark Mode Support**: Professional light and dark themes
- **Offline Capability**: IndexedDB caching for offline analysis results

## 🚀 Technology Stack

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **Shadcn/ui** - Modern component library

### AI/ML
- **MediaPipe Face Mesh** - 468-point facial landmark detection
- **OpenCV.js** - Computer vision processing
- **WebAssembly** - High-performance local processing
- **Lab Color Space** - Perceptual color analysis

### Storage
- **IndexedDB** - Local storage for offline capability
- **Browser APIs** - Camera access and file handling

## 📱 Getting Started

### Prerequisites
- Node.js 18+
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Yybe/Chromalyze-.git
   cd Chromalyze-
   ```

2. **Install frontend dependencies**
   ```bash
   cd frontend
   npm install
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```

4. **Open your browser**
   Navigate to `http://localhost:3000`

## 🎯 Usage

1. **Upload Photo**: Take a photo or upload an existing image
2. **AI Analysis**: The system analyzes facial features and color characteristics
3. **Get Results**: Receive detailed face shape and color season analysis
4. **View Recommendations**: Explore personalized beauty recommendations

## 🏗️ Project Structure

```
Chromalyze-/
├── frontend/                 # Next.js frontend application
│   ├── src/
│   │   ├── app/             # App Router pages
│   │   ├── components/      # React components
│   │   ├── lib/            # Utility functions and services
│   │   └── types/          # TypeScript type definitions
│   ├── public/             # Static assets
│   └── package.json        # Frontend dependencies
├── backend/                # Python backend (optional)
└── README.md              # Project documentation
```

## 🔧 Configuration

The application is designed to work out of the box with no additional configuration required. All processing happens locally in the browser.

### Environment Variables (Optional)
Create a `.env.local` file in the frontend directory for any custom configurations:

```env
# Optional: Custom API endpoints
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🧪 Testing

```bash
# Run frontend tests
cd frontend
npm test

# Run with coverage
npm run test:coverage
```

## 🚀 Deployment

### Vercel (Recommended)
1. Connect your GitHub repository to Vercel
2. Deploy automatically on push to main branch

### Manual Build
```bash
cd frontend
npm run build
npm start
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- MediaPipe team for facial landmark detection
- OpenCV community for computer vision tools
- Tailwind CSS for the styling framework
- Shadcn/ui for component library

## 📞 Support

For support, please open an issue on GitHub or contact the development team.

---

**Built with ❤️ for the beauty and tech community**
