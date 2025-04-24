import { useQuery } from '@tanstack/react-query';
import { searchCourses, getSubjects } from '@/lib/api';

export const useCourseSearch = (query: string, limit?: number, subject?: string) => {
  return useQuery({
    queryKey: ['courses', query, limit, subject],
    queryFn: () => searchCourses(query, limit, subject),
    enabled: query.length > 0,
  });
};

export const useSubjects = () => {
  return useQuery({
    queryKey: ['subjects'],
    queryFn: getSubjects,
  });
}; 