'use client';

import { useEffect, useRef, useState, useCallback, forwardRef, useImperativeHandle } from 'react';
import { Detection } from '@/lib/api';

// Industrial-grade color palette for each damage class
const CLASS_COLORS: Record<string, { primary: string; secondary: string; glow: string }> = {
  'Drain hole impairment': { primary: '#FF6B6B', secondary: '#FF8E8E', glow: 'rgba(255, 107, 107, 0.4)' },
  'Lightning Strike': { primary: '#FFE66D', secondary: '#FFF0A0', glow: 'rgba(255, 230, 109, 0.4)' },
  'OIL LEAKAGE': { primary: '#4ECDC4', secondary: '#7EDAD4', glow: 'rgba(78, 205, 196, 0.4)' },
  'PU-tape': { primary: '#A66CFF', secondary: '#C4A0FF', glow: 'rgba(166, 108, 255, 0.4)' },
  'Paint': { primary: '#FF9F43', secondary: '#FFB76B', glow: 'rgba(255, 159, 67, 0.4)' },
  'Surface Crack': { primary: '#EE5A5A', secondary: '#F28585', glow: 'rgba(238, 90, 90, 0.4)' },
  'dirt': { primary: '#8B7355', secondary: '#A69076', glow: 'rgba(139, 115, 85, 0.4)' },
  'le-erosion': { primary: '#00D9FF', secondary: '#66E8FF', glow: 'rgba(0, 217, 255, 0.4)' },
};

const DEFAULT_COLOR = { primary: '#00FF00', secondary: '#66FF66', glow: 'rgba(0, 255, 0, 0.4)' };

export interface BoundingBoxCanvasRef {
  downloadImage: () => void;
}

interface BoundingBoxCanvasProps {
  imageUrl: string;
  detections: Detection[];
  width?: number;
  height?: number;
  highlightedIndex?: number | null;
  enablePulse?: boolean;
}

const BoundingBoxCanvas = forwardRef<BoundingBoxCanvasRef, BoundingBoxCanvasProps>(({
  imageUrl,
  detections,
  highlightedIndex = null,
  enablePulse = true
}, ref) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const animationRef = useRef<number | null>(null);
  const [imageDimensions, setImageDimensions] = useState({ width: 0, height: 0, naturalWidth: 0, naturalHeight: 0 });
  const [pulsePhase, setPulsePhase] = useState(0);

  // Expose download method to parent via ref
  useImperativeHandle(ref, () => ({
    downloadImage: () => {
      const canvas = canvasRef.current;
      if (!canvas) return;

      canvas.toBlob((blob) => {
        if (!blob) return;
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `damage-detection-${Date.now()}.png`;
        link.click();
        URL.revokeObjectURL(url);
      }, 'image/png');
    }
  }));

  useEffect(() => {
    const img = new Image();
    img.crossOrigin = 'anonymous';
    img.onload = () => {
      const container = containerRef.current;
      if (!container) return;

      const containerWidth = container.clientWidth;
      const aspectRatio = img.naturalWidth / img.naturalHeight;
      const displayWidth = containerWidth;
      const displayHeight = containerWidth / aspectRatio;

      setImageDimensions({
        width: displayWidth,
        height: displayHeight,
        naturalWidth: img.naturalWidth,
        naturalHeight: img.naturalHeight,
      });
    };
    img.src = imageUrl;
  }, [imageUrl]);

  // Animation loop for pulse effect
  useEffect(() => {
    if (!enablePulse) return;

    let startTime: number | null = null;
    const animate = (timestamp: number) => {
      if (!startTime) startTime = timestamp;
      const elapsed = timestamp - startTime;
      setPulsePhase((elapsed / 1000) % (2 * Math.PI));
      animationRef.current = requestAnimationFrame(animate);
    };

    animationRef.current = requestAnimationFrame(animate);

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [enablePulse]);

  const drawCanvas = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas || imageDimensions.width === 0) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const img = new Image();
    img.crossOrigin = 'anonymous';
    img.onload = () => {
      // Set canvas size
      canvas.width = imageDimensions.width;
      canvas.height = imageDimensions.height;

      // Draw image
      ctx.drawImage(img, 0, 0, imageDimensions.width, imageDimensions.height);

      // Calculate scale factors
      const scaleX = imageDimensions.width / imageDimensions.naturalWidth;
      const scaleY = imageDimensions.height / imageDimensions.naturalHeight;

      // Draw bounding boxes
      detections.forEach((detection, index) => {
        const colors = CLASS_COLORS[detection.class] || DEFAULT_COLOR;
        const isHighlighted = highlightedIndex === index;

        // Scale coordinates
        const x1 = detection.bbox.x1 * scaleX;
        const y1 = detection.bbox.y1 * scaleY;
        const x2 = detection.bbox.x2 * scaleX;
        const y2 = detection.bbox.y2 * scaleY;
        const width = x2 - x1;
        const height = y2 - y1;

        // Calculate pulse effect
        const pulseScale = enablePulse ? 1 + Math.sin(pulsePhase * 2) * 0.03 : 1;
        const pulseGlow = enablePulse ? 15 + Math.sin(pulsePhase * 2) * 5 : 15;

        // Enhanced glow for highlighted box
        const glowIntensity = isHighlighted ? 30 : pulseGlow;
        const lineWidthMultiplier = isHighlighted ? 1.5 : 1;

        // Draw outer glow effect
        ctx.shadowColor = isHighlighted
          ? colors.primary.replace(')', ', 0.8)').replace('rgb', 'rgba')
          : colors.glow;
        ctx.shadowBlur = glowIntensity;
        ctx.shadowOffsetX = 0;
        ctx.shadowOffsetY = 0;

        // Draw main bounding box with thick border
        ctx.strokeStyle = colors.primary;
        ctx.lineWidth = 3 * lineWidthMultiplier * pulseScale;
        ctx.strokeRect(x1, y1, width, height);

        // Draw additional highlight ring for highlighted box
        if (isHighlighted) {
          ctx.strokeStyle = 'rgba(255, 255, 255, 0.6)';
          ctx.lineWidth = 1;
          ctx.strokeRect(x1 - 3, y1 - 3, width + 6, height + 6);
        }

        // Reset shadow for inner elements
        ctx.shadowBlur = 0;

        // Draw corner accents (industrial look)
        const cornerLength = Math.min(20, width / 4, height / 4) * pulseScale;
        const cornerThickness = (isHighlighted ? 5 : 4) * lineWidthMultiplier;

        ctx.strokeStyle = colors.secondary;
        ctx.lineWidth = cornerThickness;
        ctx.lineCap = 'square';

        // Top-left corner
        ctx.beginPath();
        ctx.moveTo(x1, y1 + cornerLength);
        ctx.lineTo(x1, y1);
        ctx.lineTo(x1 + cornerLength, y1);
        ctx.stroke();

        // Top-right corner
        ctx.beginPath();
        ctx.moveTo(x2 - cornerLength, y1);
        ctx.lineTo(x2, y1);
        ctx.lineTo(x2, y1 + cornerLength);
        ctx.stroke();

        // Bottom-left corner
        ctx.beginPath();
        ctx.moveTo(x1, y2 - cornerLength);
        ctx.lineTo(x1, y2);
        ctx.lineTo(x1 + cornerLength, y2);
        ctx.stroke();

        // Bottom-right corner
        ctx.beginPath();
        ctx.moveTo(x2 - cornerLength, y2);
        ctx.lineTo(x2, y2);
        ctx.lineTo(x2, y2 - cornerLength);
        ctx.stroke();

        // Draw label background
        const label = `${detection.class} ${(detection.confidence * 100).toFixed(0)}%`;
        ctx.font = `bold ${isHighlighted ? 14 : 12}px "Segoe UI", Arial, sans-serif`;
        const textMetrics = ctx.measureText(label);
        const textHeight = isHighlighted ? 20 : 18;
        const padding = 6;
        const labelWidth = textMetrics.width + padding * 2;
        const labelHeight = textHeight + padding;

        // Label position (above the box, or inside if no room)
        let labelX = x1;
        let labelY = y1 - labelHeight - 4;
        if (labelY < 0) {
          labelY = y1 + 4;
        }

        // Draw label background with gradient
        const gradient = ctx.createLinearGradient(labelX, labelY, labelX, labelY + labelHeight);
        gradient.addColorStop(0, colors.primary);
        gradient.addColorStop(1, colors.secondary);

        // Rounded rectangle for label
        const radius = 4;
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.moveTo(labelX + radius, labelY);
        ctx.lineTo(labelX + labelWidth - radius, labelY);
        ctx.quadraticCurveTo(labelX + labelWidth, labelY, labelX + labelWidth, labelY + radius);
        ctx.lineTo(labelX + labelWidth, labelY + labelHeight - radius);
        ctx.quadraticCurveTo(labelX + labelWidth, labelY + labelHeight, labelX + labelWidth - radius, labelY + labelHeight);
        ctx.lineTo(labelX + radius, labelY + labelHeight);
        ctx.quadraticCurveTo(labelX, labelY + labelHeight, labelX, labelY + labelHeight - radius);
        ctx.lineTo(labelX, labelY + radius);
        ctx.quadraticCurveTo(labelX, labelY, labelX + radius, labelY);
        ctx.closePath();
        ctx.fill();

        // Draw label border (brighter when highlighted)
        ctx.strokeStyle = isHighlighted ? 'rgba(255, 255, 255, 0.8)' : 'rgba(255, 255, 255, 0.3)';
        ctx.lineWidth = isHighlighted ? 2 : 1;
        ctx.stroke();

        // Draw label text with shadow for readability
        ctx.shadowColor = 'rgba(0, 0, 0, 0.5)';
        ctx.shadowBlur = 2;
        ctx.shadowOffsetX = 1;
        ctx.shadowOffsetY = 1;
        ctx.fillStyle = '#FFFFFF';
        ctx.textBaseline = 'middle';
        ctx.fillText(label, labelX + padding, labelY + labelHeight / 2 + 1);
        ctx.shadowBlur = 0;
      });
    };
    img.src = imageUrl;
  }, [imageUrl, detections, imageDimensions, highlightedIndex, pulsePhase, enablePulse]);

  useEffect(() => {
    drawCanvas();
  }, [drawCanvas]);

  return (
    <div ref={containerRef} className="w-full">
      <canvas
        ref={canvasRef}
        className="w-full h-auto rounded-lg"
        style={{ maxHeight: '500px', objectFit: 'contain' }}
      />
    </div>
  );
});

BoundingBoxCanvas.displayName = 'BoundingBoxCanvas';

export default BoundingBoxCanvas;
