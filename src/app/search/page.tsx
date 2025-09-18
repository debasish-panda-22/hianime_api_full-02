"use client";

import { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import { Search, Loader2, Grid, List } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useSearchAnime, useSuggestions } from "@/hooks/useAnimeData";
import { Anime } from "@/lib/api";

const AnimeCard = ({ anime }: { anime: Anime }) => {
  const episodeCount = anime.episodes?.eps || 0;
  const hasSub = anime.episodes?.sub !== null;
  const hasDub = anime.episodes?.dub !== null;

  return (
    <Card className="group cursor-pointer hover:shadow-lg transition-all duration-200">
      <CardContent className="p-0">
        <div className="aspect-[2/3] bg-gradient-to-br from-primary/20 to-primary/5 rounded-t-lg flex items-center justify-center relative overflow-hidden">
          {anime.poster ? (
            <img 
              src={anime.poster} 
              alt={anime.title}
              className="w-full h-full object-cover"
            />
          ) : (
            <div className="text-center text-muted-foreground">
              <div className="text-4xl mb-2">🎬</div>
              <p className="text-xs">Cover</p>
            </div>
          )}
          <div className="absolute top-2 right-2 bg-black/80 text-white px-2 py-1 rounded text-xs font-semibold">
            {anime.rating || 'N/A'}
          </div>
          <div className="absolute bottom-2 left-2 flex gap-1">
            {hasSub && <Badge variant="secondary" className="text-xs">SUB</Badge>}
            {hasDub && <Badge variant="secondary" className="text-xs">DUB</Badge>}
          </div>
        </div>
        <div className="p-4 space-y-2">
          <h3 className="font-semibold text-sm line-clamp-2">{anime.title}</h3>
          <div className="flex items-center justify-between text-xs text-muted-foreground">
            <span>{episodeCount} eps</span>
            <Badge variant="outline" className="text-xs">
              {anime.type}
            </Badge>
          </div>
          <div className="flex items-center justify-between text-xs text-muted-foreground">
            <span>{anime.duration}</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

const AnimeListItem = ({ anime }: { anime: Anime }) => {
  const episodeCount = anime.episodes?.eps || 0;
  const hasSub = anime.episodes?.sub !== null;
  const hasDub = anime.episodes?.dub !== null;

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardContent className="p-4">
        <div className="flex space-x-4">
          <div className="flex-shrink-0">
            <div className="w-24 h-32 bg-gradient-to-br from-primary/20 to-primary/5 rounded flex items-center justify-center relative overflow-hidden">
              {anime.poster ? (
                <img 
                  src={anime.poster} 
                  alt={anime.title}
                  className="w-full h-full object-cover"
                />
              ) : (
                <div className="text-center text-muted-foreground">
                  <div className="text-2xl mb-1">🎬</div>
                  <p className="text-xs">Cover</p>
                </div>
              )}
            </div>
          </div>
          <div className="flex-1 space-y-2">
            <div className="flex items-start justify-between">
              <h3 className="font-semibold text-lg line-clamp-2">{anime.title}</h3>
              <div className="bg-black/80 text-white px-2 py-1 rounded text-xs font-semibold">
                {anime.rating || 'N/A'}
              </div>
            </div>
            {anime.alternativeTitle && (
              <p className="text-sm text-muted-foreground line-clamp-1">{anime.alternativeTitle}</p>
            )}
            <div className="flex items-center space-x-4 text-sm text-muted-foreground">
              <span>{episodeCount} episodes</span>
              <span>{anime.duration}</span>
              <Badge variant="outline">{anime.type}</Badge>
            </div>
            <div className="flex items-center space-x-2">
              {hasSub && <Badge variant="secondary" className="text-xs">SUB</Badge>}
              {hasDub && <Badge variant="secondary" className="text-xs">DUB</Badge>}
            </div>
          </div>
          <div className="flex items-center">
            <Button size="sm">
              Watch Now
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default function SearchPage() {
  const searchParams = useSearchParams();
  const initialQuery = searchParams.get('q') || '';
  
  const [searchQuery, setSearchQuery] = useState(initialQuery);
  const [currentPage, setCurrentPage] = useState(1);
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [sortBy, setSortBy] = useState('default');
  const [showSuggestions, setShowSuggestions] = useState(false);
  
  const { data: searchData, loading, error } = useSearchAnime(searchQuery, currentPage);
  const { suggestions, loading: suggestionsLoading } = useSuggestions(searchQuery);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setCurrentPage(1);
  };

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Search Header */}
      <div className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-40">
        <div className="container mx-auto px-4 py-6">
          <div className="max-w-2xl mx-auto">
            <form onSubmit={handleSearch} className="relative">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                placeholder="Search for anime..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onFocus={() => setShowSuggestions(true)}
                onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
                className="pl-10 pr-4 h-12 text-lg"
              />
              {showSuggestions && suggestions.length > 0 && (
                <div className="absolute top-full left-0 right-0 mt-1 bg-background border rounded-md shadow-lg z-50 max-h-60 overflow-y-auto">
                  {suggestionsLoading ? (
                    <div className="p-2 text-center text-muted-foreground">
                      <Loader2 className="h-4 w-4 animate-spin inline" />
                    </div>
                  ) : (
                    suggestions.map((suggestion, index) => (
                      <div
                        key={index}
                        className="px-3 py-2 hover:bg-muted cursor-pointer text-sm"
                        onMouseDown={() => {
                          setSearchQuery(suggestion);
                          setShowSuggestions(false);
                        }}
                      >
                        {suggestion}
                      </div>
                    ))
                  )}
                </div>
              )}
              <Button type="submit" className="absolute right-2 top-1/2 -translate-y-1/2" size="sm">
                Search
              </Button>
            </form>
          </div>
        </div>
      </div>

      {/* Filters and Controls */}
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <span className="text-sm font-medium">Sort by:</span>
              <Select value={sortBy} onValueChange={setSortBy}>
                <SelectTrigger className="w-32">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="default">Default</SelectItem>
                  <SelectItem value="rating">Rating</SelectItem>
                  <SelectItem value="title">Title</SelectItem>
                  <SelectItem value="episodes">Episodes</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <Button
              variant={viewMode === 'grid' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setViewMode('grid')}
            >
              <Grid className="h-4 w-4" />
            </Button>
            <Button
              variant={viewMode === 'list' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setViewMode('list')}
            >
              <List className="h-4 w-4" />
            </Button>
          </div>
        </div>

        {/* Results Info */}
        {searchData && (
          <div className="mb-6">
            <h1 className="text-2xl font-bold mb-2">
              Search Results for "{searchQuery}"
            </h1>
            <p className="text-muted-foreground">
              Found {searchData.response.length} results (Page {currentPage} of {searchData.pageInfo.totalPages})
            </p>
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="h-8 w-8 animate-spin" />
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="text-center py-12">
            <h2 className="text-xl font-semibold mb-2">Error loading results</h2>
            <p className="text-muted-foreground mb-4">{error}</p>
            <Button onClick={() => window.location.reload()}>
              Try Again
            </Button>
          </div>
        )}

        {/* No Results */}
        {searchData && searchData.response.length === 0 && (
          <div className="text-center py-12">
            <h2 className="text-xl font-semibold mb-2">No results found</h2>
            <p className="text-muted-foreground">
              Try searching with different keywords or check your spelling.
            </p>
          </div>
        )}

        {/* Results Grid/List */}
        {searchData && searchData.response.length > 0 && (
          <>
            {viewMode === 'grid' ? (
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-6">
                {searchData.response.map((anime) => (
                  <AnimeCard key={anime.id} anime={anime} />
                ))}
              </div>
            ) : (
              <div className="space-y-4">
                {searchData.response.map((anime) => (
                  <AnimeListItem key={anime.id} anime={anime} />
                ))}
              </div>
            )}

            {/* Pagination */}
            {searchData.pageInfo.totalPages > 1 && (
              <div className="flex items-center justify-center space-x-2 mt-8">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handlePageChange(currentPage - 1)}
                  disabled={currentPage <= 1}
                >
                  Previous
                </Button>
                
                <div className="flex items-center space-x-1">
                  {Array.from({ length: Math.min(searchData.pageInfo.totalPages, 5) }, (_, i) => {
                    const page = i + 1;
                    return (
                      <Button
                        key={page}
                        variant={currentPage === page ? 'default' : 'outline'}
                        size="sm"
                        onClick={() => handlePageChange(page)}
                      >
                        {page}
                      </Button>
                    );
                  })}
                </div>
                
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handlePageChange(currentPage + 1)}
                  disabled={currentPage >= searchData.pageInfo.totalPages}
                >
                  Next
                </Button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}