/**
 * API client for backend communication
 */

import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface Detection {
  class: string;
  confidence: number;
  bbox: {
    x1: number;
    y1: number;
    x2: number;
    y2: number;
  };
}

export interface InferenceResponse {
  success: boolean;
  message: string;
  total_detections: number;
  damages_found: string[];
  damage_counts: Record<string, number>;
  detections: Detection[];
  annotated_image?: string;
}

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});

export async function predictDamage(
  file: File,
  conf: number = 0.25,
  iou: number = 0.45,
  imgsz: number = 640
): Promise<InferenceResponse> {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('conf', conf.toString());
  formData.append('iou', iou.toString());
  formData.append('imgsz', imgsz.toString());

  const response = await apiClient.post<InferenceResponse>(
    '/api/inference/predict',
    formData
  );

  return response.data;
}

export async function getDamageClasses(): Promise<string[]> {
  const response = await apiClient.get<{ classes: string[] }>(
    '/api/inference/classes'
  );
  return response.data.classes;
}
