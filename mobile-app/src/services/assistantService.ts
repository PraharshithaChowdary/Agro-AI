import { apiClient } from './api';
import { ChatMessage, EvidenceSource, AssistantEngineStatus, SessionSummary } from '../types';

export interface ChatResponse {
  response: string;
  category: 'crop_care' | 'soil' | 'disease' | 'nutrition' | 'irrigation' | 'economics' | 'general' | 'clarification';
  sessionId?: string;
  suggestedQuestions?: string[];
  evidenceSources?: EvidenceSource[];
  calculatorData?: any;
  modelProvider?: string;
  savedToAccount?: boolean;
  persistenceMessage?: string;
  relatedAction?: {
    label: string;
    route: string;
  };
}

export const assistantService = {
  async sendMessage(
    message: string,
    history: ChatMessage[] = [],
    sessionId?: string
  ): Promise<ChatResponse> {
    try {
      const res = await apiClient.post<ChatResponse>('/assistant/chat', {
        message,
        sessionId,
        history: history.slice(-6).map((h) => ({
          sender: h.sender,
          content: h.content,
        })),
      });
      return res.data;
    } catch (err: any) {
      if (err.response?.data?.detail) {
        throw new Error(err.response.data.detail);
      }
      throw new Error(err.message || 'AGRO AI Assistant is unavailable. Please check the backend connection and try again.');
    }
  },

  async getEngineStatus(): Promise<AssistantEngineStatus> {
    try {
      const res = await apiClient.get<AssistantEngineStatus>('/assistant/status');
      return res.data;
    } catch {
      return {
        provider: 'offline',
        model: 'Unavailable',
        is_live_llm: false,
        mode: 'Backend status unavailable — connect to the AGRO AI API to request guidance',
        badge: 'Backend unavailable'
      };
    }
  },

  async getSessions(): Promise<SessionSummary[]> {
    try {
      const res = await apiClient.get<SessionSummary[]>('/assistant/sessions');
      return res.data;
    } catch {
      return [];
    }
  },

  async getSessionHistory(sessionId: string): Promise<ChatMessage[]> {
    try {
      const res = await apiClient.get<any[]>(`/assistant/sessions/${sessionId}`);
      return res.data.map((m) => ({
        id: m.id,
        sender: m.sender,
        content: m.content,
        timestamp: m.createdAt,
        category: m.category,
        evidenceSources: m.evidenceSources,
        calculatorData: m.calculatorData,
      }));
    } catch {
      return [];
    }
  },

  async clearSession(sessionId: string): Promise<void> {
    try {
      await apiClient.delete(`/assistant/sessions/${sessionId}`);
    } catch (err) {
      console.warn('Failed to clear session on server:', err);
    }
  },

  async executeCalculation(calcType: string, params: Record<string, any>): Promise<any> {
    const res = await apiClient.post('/assistant/calculate', {
      calcType,
      params,
    });
    return res.data;
  },

  async updateConfig(provider: string, model?: string, apiKey?: string): Promise<AssistantEngineStatus> {
    const res = await apiClient.post<AssistantEngineStatus>('/assistant/config', {
      provider,
      model,
      apiKey,
    });
    return res.data;
  },

  async resetConfig(): Promise<AssistantEngineStatus> {
    const res = await apiClient.delete<AssistantEngineStatus>('/assistant/config');
    return res.data;
  },


};
