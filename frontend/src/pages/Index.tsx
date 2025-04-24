
import { SearchBar } from "@/components/SearchBar";
import { SearchSuggestions } from "@/components/SearchSuggestions";
import { Footer } from "@/components/Footer";

const Index = () => {
  return (
    <div className="min-h-screen flex flex-col bg-cornell-warm">
      <main className="flex-1 flex flex-col items-center px-4">
        <div className="w-full max-w-4xl mx-auto text-center mt-20 mb-16">
          <h1 className="text-4xl md:text-5xl font-bold text-cornell-red mb-4">
            Cornell Class Search
          </h1>
          <p className="text-lg text-gray-600 mb-8 max-w-2xl mx-auto">
            Find the perfect classes using our semantic search engine. Discover courses
            based on concepts, topics, and natural language queries.
          </p>
          <SearchBar />
          <SearchSuggestions />
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default Index;
