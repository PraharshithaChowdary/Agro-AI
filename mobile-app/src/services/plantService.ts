import { apiClient } from './api';
import {
  PlantSearchResponse,
  PlantCategoryCount,
  PlantSpeciesRecord,
  PlantIdentificationResult,
  PlantHealthAnalysisResult,
  PlantAutocompleteItem
} from '../types';

export const plantService = {
  /**
   * Fast botanical autocomplete across the bundled plant catalogue
   */
  async autocompletePlants(query: string, limit: number = 10): Promise<PlantAutocompleteItem[]> {
    if (!query || !query.trim()) return [];
    const response = await apiClient.get<PlantAutocompleteItem[]>('/plants/autocomplete', {
      params: { q: query.trim(), limit },
    });
    return response.data;
  },

  /**
   * Search Indian plant species with pagination and filters
   */
  async searchPlants(
    query?: string,
    category?: string,
    state?: string,
    page: number = 1,
    limit: number = 20
  ): Promise<PlantSearchResponse> {
    const params: Record<string, any> = { page, limit };
    if (query && query.trim()) params.q = query.trim();
    if (category && category.trim()) params.category = category.trim();
    if (state && state.trim()) params.state = state.trim();

    const response = await apiClient.get<PlantSearchResponse>('/plants/search', { params });
    return response.data;
  },

  /**
   * Get list of categories and counts
   */
  async getCategories(): Promise<PlantCategoryCount[]> {
    const response = await apiClient.get<PlantCategoryCount[]>('/plants/categories');
    return response.data;
  },

  /**
   * Get catalog high-level stats
   */
  async getCatalogStats(): Promise<{
    totalVerifiedSpecies: number;
    targetSpeciesGoal: number;
    toxicOrPoisonousSpecies: number;
    supportedDiseaseCrops: number;
    status: string;
  }> {
    const response = await apiClient.get('/plants/stats');
    return response.data;
  },

  /**
   * Retrieve full plant details by ID
   */
  async getPlantDetails(plantId: string): Promise<PlantSpeciesRecord> {
    const response = await apiClient.get<PlantSpeciesRecord>(`/plants/${encodeURIComponent(plantId)}`);
    return response.data;
  },

  /**
   * Identify plant image (Mode A: Automatic or Mode B: By Name)
   */
  async identifyPlant(
    imageFile: File,
    plantName?: string,
    organ: string = 'leaf'
  ): Promise<PlantIdentificationResult> {
    const formData = new FormData();
    formData.append('image', imageFile);
    if (plantName && plantName.trim()) {
      formData.append('plant_name', plantName.trim());
    }
    formData.append('organ', organ);

    const response = await apiClient.post<PlantIdentificationResult>('/plants/identify', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      // CPU-only Codespaces may need longer to load and run the vision model.
      timeout: 420000,
    });
    return response.data;
  },

  /**
   * Execute dedicated plant health analysis
   */
  async analyzePlantHealth(
    imageFile: File,
    plantId?: string,
    plantName?: string
  ): Promise<PlantHealthAnalysisResult> {
    const formData = new FormData();
    formData.append('image', imageFile);
    if (plantId && plantId.trim()) {
      formData.append('plant_id', plantId.trim());
    }
    if (plantName && plantName.trim()) {
      formData.append('plant_name', plantName.trim());
    }

    const response = await apiClient.post<PlantHealthAnalysisResult>('/plants/analyze-health', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 420000,
    });
    return response.data;
  },
};
