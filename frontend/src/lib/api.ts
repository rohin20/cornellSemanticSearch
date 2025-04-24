import axios from 'axios';

// Types
export interface Course {
  id: string;
  subject: string;
  title: string;
  description: string;
  relevance_score: number;
}

export interface SearchResponse {
  results: Course[];
}

export interface SubjectsResponse {
  subjects: string[];
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

// Create axios instance
export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API functions
export const searchCourses = async (
  query: string,
  limit?: number,
  subject_filter?: string
) => {
  const params = new URLSearchParams();
  params.append('query', query);
  if (limit) params.append('limit', limit.toString());
  if (subject_filter) params.append('subject_filter', subject_filter);

  const response = await api.get<SearchResponse>(`/search?${params.toString()}`);
  return response.data;
};

export const getSubjects = async () => {
  const response = await api.get<SubjectsResponse>('/subjects');
  return response.data;
}; 