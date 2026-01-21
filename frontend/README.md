# Offshore Wind Damage Detection - Frontend

Next.js frontend for the offshore wind turbine blade damage detection system.

## Features

- 🎨 Modern UI matching the Mira Intel design
- 📤 Drag-and-drop image upload
- 🔍 Real-time damage detection visualization
- 📊 Detailed detection results display
- 💾 Download results functionality
- 📱 Responsive design

## Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

Create a `.env.local` file:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Build for Production

```bash
npm run build
npm start
```

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx           # Root layout with metadata
│   ├── page.tsx             # Main detection page
│   └── globals.css          # Global styles
├── components/
│   ├── Navbar.tsx           # Navigation bar
│   ├── ImageUpload.tsx      # Drag-and-drop upload component
│   └── DetectionResults.tsx # Results display component
├── lib/
│   └── api.ts               # API client functions
└── public/                  # Static assets
```

## Components

### ImageUpload
Handles drag-and-drop and click-to-upload functionality for blade images.

### DetectionResults
Displays detected damages with confidence scores and bounding box information.

### Navbar
Navigation component with Mira Intel branding.

## API Integration

The frontend communicates with the backend API at `NEXT_PUBLIC_API_URL`.

Main API calls:
- `POST /api/inference/predict` - Upload image for damage detection
- `GET /api/inference/classes` - Get list of detectable damage types

## Styling

- **Framework**: TailwindCSS
- **Colors**:
  - Navy: `#1e3a5f` (mira-navy)
  - Blue: `#4a90e2` (mira-blue)
- **Fonts**: System defaults

## Deployment

### Docker

```bash
docker build -t offshore-wind-frontend .
docker run -p 3000:3000 offshore-wind-frontend
```

### Vercel (Recommended)

```bash
vercel deploy
```

Set environment variable `NEXT_PUBLIC_API_URL` in Vercel dashboard.
