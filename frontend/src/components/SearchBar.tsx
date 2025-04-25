import { Search } from "lucide-react";
import { Input } from "./ui/input";
import { Button } from "./ui/button";
import { useState, useEffect } from "react";
import { useCourseSearch } from "@/hooks/useCourseSearch";
import { Card } from "./ui/card";
import { Skeleton } from "./ui/skeleton";

export const SearchBar = () => {
  const [query, setQuery] = useState("");
  const [debouncedQuery, setDebouncedQuery] = useState("");
  const { data, isLoading, error } = useCourseSearch(debouncedQuery);

  // Debounce effect
  useEffect(() => {
    const timerId = setTimeout(() => {
      setDebouncedQuery(query);
    }, 750); // 0.75 seconds

    return () => {
      clearTimeout(timerId);
    };
  }, [query]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    // Force immediate search on button click
    setDebouncedQuery(query);
  };

  return (
    <div className="flex flex-col items-center w-full gap-6">
      <form onSubmit={handleSearch} className="relative w-full max-w-2xl">
        <Input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search for fa24 classes (e.g., 'python for hotelies' or 'wines')"
          className="w-full pl-4 pr-12 py-6 text-lg border-2 border-gray-200 rounded-lg focus:border-cornell-red focus:ring-0"
        />
        <Button
          type="submit"
          className="absolute right-2 top-1/2 -translate-y-1/2 bg-cornell-red hover:bg-cornell-red/90"
          size="icon"
        >
          <Search className="h-5 w-5" />
        </Button>
      </form>

      {/* Search Results */}
      <div className="w-full max-w-3xl space-y-4">
        {isLoading ? (
          // Loading skeletons
          Array.from({ length: 3 }).map((_, i) => (
            <Card key={i} className="p-4">
              <Skeleton className="h-6 w-1/3 mb-2" />
              <Skeleton className="h-4 w-full" />
            </Card>
          ))
        ) : error ? (
          <Card className="p-4 bg-red-50 border-red-200">
            <p className="text-red-600">Error: {error.message}</p>
          </Card>
        ) : data?.results.length ? (
          // Search results
          data.results.map((course) => (
            <Card key={course.id} className="p-4 hover:shadow-md transition-shadow">
              <h3 className="font-semibold text-lg">
                {course.subject}: {course.title}
              </h3>
              <p className="text-gray-600 mt-1">{course.description}</p>
              <div className="mt-2 text-sm text-gray-500">
                Relevance: {Math.round(course.relevance_score * 100)}%
              </div>
            </Card>
          ))
        ) : query.length > 0 ? (
          <p className="text-center text-gray-600">No results found. Try a different search term.</p>
        ) : null}
      </div>
    </div>
  );
};