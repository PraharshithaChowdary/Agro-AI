import { apiClient } from './api';
import {
  CropAnalysisResult,
  SoilAnalysisResult,
  ProductionHistoryItem,
  NamedPlantAnalysisResult,
  SupportedPlantItem
} from '../types';

export const productionService = {
  async analyzeNamedPlant(
    imageFile: File,
    plantName: string,
    cropType?: string,
    growingLocation?: string
  ): Promise<NamedPlantAnalysisResult> {
    const formData = new FormData();
    formData.append('image', imageFile);
    formData.append('plant_name', plantName);
    if (cropType) formData.append('crop_type', cropType);
    if (growingLocation) formData.append('growing_location', growingLocation);

    try {
      const response = await apiClient.post<NamedPlantAnalysisResult>(
        '/production/analyze-named-plant',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          timeout: 420000, // Allow time for CPU-only Ollama vision inference.
        }
      );
      return response.data;
    } catch (err: any) {
      if (err.response?.data?.detail) {
        throw new Error(err.response.data.detail);
      }
      throw new Error(err.message || 'Plant health analysis failed');
    }
  },

  async getSupportedPlants(): Promise<SupportedPlantItem[]> {
    try {
      const response = await apiClient.get<SupportedPlantItem[]>('/production/supported-plants');
      return response.data;
    } catch (err: any) {
      return [];
    }
  },

  async analyzeCrop(imageFile: File): Promise<CropAnalysisResult> {
    const formData = new FormData();
    formData.append('image', imageFile);

    try {
      const response = await apiClient.post<CropAnalysisResult>('/production/crop-analysis', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 420000, // Allow time for CPU-only Ollama vision inference.
      });
      return response.data;
    } catch (err: any) {
      if (err.response?.data?.detail) {
        throw new Error(err.response.data.detail);
      }
      throw new Error(err.message || 'Crop analysis failed');
    }
  },

  async analyzeSoil(imageFile: File): Promise<SoilAnalysisResult> {
    const formData = new FormData();
    formData.append('image', imageFile);

    try {
      const response = await apiClient.post<SoilAnalysisResult>('/production/soil-analysis', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 420000, // Allow time for CPU-only Ollama vision inference.
      });
      return response.data;
    } catch (err: any) {
      if (err.response?.data?.detail) {
        throw new Error(err.response.data.detail);
      }
      throw new Error(err.message || 'Soil analysis failed');
    }
  },

  async getHistory(): Promise<ProductionHistoryItem[]> {
    try {
      const response = await apiClient.get<ProductionHistoryItem[]>('/production/history');
      return response.data;
    } catch (err: any) {
      return [];
    }
  },
};

