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

// Use the base URL directly without /api suffix
const API_BASE_URL = "https://cornellsemanticsearch.onrender.com";

// Create axios instance
export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add response interceptor for logging
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.data);
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// API functions
export const searchCourses = async (
  query: string,
  limit?: number,
  subject_filter?: string
) => {
  try {
    console.log('Making search request with params:', { query, limit, subject_filter });
    const params = new URLSearchParams();
    params.append('query', query);
    if (limit) params.append('limit', limit.toString());
    if (subject_filter) params.append('subject_filter', subject_filter);

    const response = await api.get<SearchResponse>(`/search?${params.toString()}`);
    console.log('Search response:', response.data);
    return response.data;
  } catch (error) {
    console.error('Search error:', error);
    throw error;
  }
};

export const getSubjects = async () => {
  const response = await api.get<SubjectsResponse>('/subjects');
  return response.data;
}; 