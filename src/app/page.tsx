"use client";

import { useState } from "react";
import { Search, Play, Plus, Star, Clock, TrendingUp, Calendar, Loader2, Moon, Sun } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useTheme } from "next-themes";
import { useHomepageData, useSearchAnime, useAnimeList, useSuggestions } from "@/hooks/useAnimeData";
import { Anime } from "@/lib/api";

// Anime card component
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

// Search component with suggestions
const SearchBar = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [showSuggestions, setShowSuggestions] = useState(false);
  const { suggestions, loading } = useSuggestions(searchQuery);

  return (
    <div className="relative">
      <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
      <Input
        placeholder="Search anime..."
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        onFocus={() => setShowSuggestions(true)}
        onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
        className="w-64 pl-10"
      />
      {showSuggestions && suggestions.length > 0 && (
        <div className="absolute top-full left-0 right-0 mt-1 bg-background border rounded-md shadow-lg z-50 max-h-60 overflow-y-auto">
          {loading ? (
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
    </div>
  );
};

export default function Home() {
  const { theme, setTheme } = useTheme();
  const { data: homepageData, loading, error } = useHomepageData();
  const { data: searchData, loading: searchLoading } = useSearchAnime("");
  const { data: popularData } = useAnimeList("most-popular");
  const { data: trendingData } = useAnimeList("top-airing");

  // Mock data for sections that might not be available in API
  const upcomingSchedule = [
    { day: "Monday", anime: ["One Piece Episode 1075", "Black Clover Episode 171"] },
    { day: "Tuesday", anime: ["My Hero Academia Season 7", "Jujutsu Kaisen Season 3"] },
    { day: "Wednesday", anime: ["Demon Slayer Season 4", "Attack on Titan Final"] },
    { day: "Thursday", anime: ["Chainsaw Man Season 2", "Spy x Family Part 3"] },
    { day: "Friday", anime: ["Blue Lock Season 2", "Tokyo Revengers Final"] },
    { day: "Saturday", anime: ["Naruto Shippuden Movie", "Boruto Next Generations"] },
    { day: "Sunday", anime: ["One Piece Film Red", "Demon Slayer Movie"] }
  ];

  const latestEpisodes = [
    { id: 11, title: "One Piece", episode: "Episode 1075", time: "2 hours ago" },
    { id: 12, title: "My Hero Academia", episode: "Episode 114", time: "5 hours ago" },
    { id: 13, title: "Jujutsu Kaisen", episode: "Episode 25", time: "1 day ago" },
    { id: 14, title: "Demon Slayer", episode: "Episode 27", time: "1 day ago" }
  ];

  // Get featured anime from spotlight or first popular anime
  const featuredAnime = homepageData?.spotlight?.[0] || popularData?.response?.[0];

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-xl font-semibold mb-2">Error loading data</h2>
          <p className="text-muted-foreground">{error}</p>
          <Button onClick={() => window.location.reload()} className="mt-4">
            Retry
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Navigation */}
      <nav className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container mx-auto px-4">
          <div className="flex h-16 items-center justify-between">
            <div className="flex items-center space-x-4">
              <h1 className="text-2xl font-bold text-primary">HiAnime</h1>
              <div className="hidden md:flex space-x-6">
                <a href="#" className="text-muted-foreground hover:text-foreground transition-colors">Home</a>
                <a href="#" className="text-muted-foreground hover:text-foreground transition-colors">Browse</a>
                <a href="#" className="text-muted-foreground hover:text-foreground transition-colors">Schedule</a>
                <a href="#" className="text-muted-foreground hover:text-foreground transition-colors">Popular</a>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <SearchBar />
              <Button
                variant="outline"
                size="sm"
                onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
              >
                {theme === "dark" ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
              </Button>
              <Button variant="outline" size="sm">
                Login
              </Button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      {featuredAnime && (
        <section className="relative h-[600px] bg-gradient-to-b from-primary/10 to-background">
          <div className="container mx-auto px-4 h-full">
            <div className="grid h-full grid-cols-1 lg:grid-cols-2 gap-8 items-center">
              <div className="space-y-6">
                <Badge variant="secondary" className="w-fit">Featured Anime</Badge>
                <h1 className="text-5xl font-bold">{featuredAnime.title}</h1>
                <p className="text-xl text-muted-foreground">
                  {featuredAnime.alternativeTitle || featuredAnime.title}
                </p>
                <div className="flex items-center space-x-4 text-muted-foreground">
                  <div className="flex items-center space-x-1">
                    <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                    <span>{featuredAnime.rating || 'N/A'}</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <Clock className="h-4 w-4" />
                    <span>{featuredAnime.episodes?.eps || 0} Episodes</span>
                  </div>
                  <Badge variant="outline">{featuredAnime.type}</Badge>
                </div>
                <div className="flex space-x-4">
                  <Button size="lg" className="bg-primary hover:bg-primary/90">
                    <Play className="mr-2 h-4 w-4" />
                    Watch Now
                  </Button>
                  <Button size="lg" variant="outline">
                    <Plus className="mr-2 h-4 w-4" />
                    Add to List
                  </Button>
                </div>
              </div>
              <div className="relative">
                <div className="aspect-[2/3] w-full max-w-md mx-auto rounded-lg overflow-hidden">
                  {featuredAnime.poster ? (
                    <img 
                      src={featuredAnime.poster} 
                      alt={featuredAnime.title}
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <div className="w-full h-full bg-gradient-to-br from-primary/20 to-primary/5 flex items-center justify-center">
                      <div className="text-center text-muted-foreground">
                        <div className="text-6xl mb-2">🥷</div>
                        <p>Anime Cover Image</p>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <Tabs defaultValue="popular" className="w-full">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="popular">Popular</TabsTrigger>
            <TabsTrigger value="trending">Trending</TabsTrigger>
            <TabsTrigger value="schedule">Schedule</TabsTrigger>
            <TabsTrigger value="latest">Latest Episodes</TabsTrigger>
          </TabsList>

          <TabsContent value="popular" className="mt-8">
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-6">
              {popularData?.response?.map((anime) => (
                <AnimeCard key={anime.id} anime={anime} />
              )) || homepageData?.mostPopular?.map((anime) => (
                <AnimeCard key={anime.id} anime={anime} />
              )) || (
                <div className="col-span-full text-center text-muted-foreground">
                  No popular anime available
                </div>
              )}
            </div>
          </TabsContent>

          <TabsContent value="trending" className="mt-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h2 className="text-2xl font-bold mb-4 flex items-center">
                  <TrendingUp className="mr-2 h-5 w-5" />
                  Trending Now
                </h2>
                <div className="space-y-4">
                  {trendingData?.response?.slice(0, 5).map((anime, index) => (
                    <Card key={anime.id} className="hover:shadow-md transition-shadow">
                      <CardContent className="p-4">
                        <div className="flex items-center space-x-4">
                          <div className="text-2xl font-bold text-primary">#{index + 1}</div>
                          <div className="flex-1">
                            <h3 className="font-semibold">{anime.title}</h3>
                            <div className="flex items-center space-x-4 text-sm text-muted-foreground">
                              <div className="flex items-center space-x-1">
                                <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                                <span>{anime.rating || 'N/A'}</span>
                              </div>
                              <span>{anime.episodes?.eps || 0} episodes</span>
                            </div>
                          </div>
                          <Button size="sm" variant="outline">
                            <Play className="h-4 w-4" />
                          </Button>
                        </div>
                      </CardContent>
                    </Card>
                  )) || (
                    <div className="text-center text-muted-foreground">
                      No trending anime available
                    </div>
                  )}
                </div>
              </div>

              <div>
                <h2 className="text-2xl font-bold mb-4">Top 10 This Week</h2>
                <div className="space-y-3">
                  {popularData?.response?.slice(0, 10).map((anime, index) => (
                    <div key={anime.id} className="flex items-center space-x-3 p-3 rounded-lg hover:bg-muted/50 transition-colors">
                      <div className="text-lg font-bold text-primary w-8">{index + 1}</div>
                      <div className="flex-1">
                        <h4 className="font-medium text-sm">{anime.title}</h4>
                        <div className="flex items-center space-x-2 text-xs text-muted-foreground">
                          <Star className="h-3 w-3 fill-yellow-400 text-yellow-400" />
                          <span>{anime.rating || 'N/A'}</span>
                        </div>
                      </div>
                      <Badge variant="outline" className="text-xs">
                        {anime.type}
                      </Badge>
                    </div>
                  )) || (
                    <div className="text-center text-muted-foreground">
                      No top anime available
                    </div>
                  )}
                </div>
              </div>
            </div>
          </TabsContent>

          <TabsContent value="schedule" className="mt-8">
            <div>
              <h2 className="text-2xl font-bold mb-6 flex items-center">
                <Calendar className="mr-2 h-5 w-5" />
                Upcoming Schedule
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                {upcomingSchedule.map((schedule) => (
                  <Card key={schedule.day}>
                    <CardContent className="p-4">
                      <h3 className="font-semibold mb-3 text-primary">{schedule.day}</h3>
                      <div className="space-y-2">
                        {schedule.anime.map((anime, index) => (
                          <div key={index} className="flex items-center space-x-2 text-sm">
                            <div className="w-2 h-2 bg-primary rounded-full"></div>
                            <span className="text-muted-foreground">{anime}</span>
                          </div>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          </TabsContent>

          <TabsContent value="latest" className="mt-8">
            <div>
              <h2 className="text-2xl font-bold mb-6">Latest Episodes</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {latestEpisodes.map((episode) => (
                  <Card key={episode.id} className="hover:shadow-md transition-shadow">
                    <CardContent className="p-4">
                      <div className="flex items-center space-x-4">
                        <div className="aspect-video w-32 bg-gradient-to-br from-primary/20 to-primary/5 rounded flex items-center justify-center">
                          <div className="text-center text-muted-foreground">
                            <div className="text-2xl mb-1">📺</div>
                            <p className="text-xs">Thumbnail</p>
                          </div>
                        </div>
                        <div className="flex-1">
                          <h3 className="font-semibold">{episode.title}</h3>
                          <p className="text-sm text-muted-foreground">{episode.episode}</p>
                          <p className="text-xs text-muted-foreground">{episode.time}</p>
                        </div>
                        <Button size="sm">
                          <Play className="h-4 w-4" />
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          </TabsContent>
        </Tabs>
      </main>

      {/* Footer */}
      <footer className="border-t bg-muted/50 mt-16">
        <div className="container mx-auto px-4 py-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <h3 className="font-semibold mb-4">HiAnime</h3>
              <p className="text-sm text-muted-foreground">
                Your ultimate destination for streaming anime online. Watch thousands of episodes in HD quality.
              </p>
            </div>
            <div>
              <h4 className="font-medium mb-4">Browse</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><a href="#" className="hover:text-foreground">Popular Anime</a></li>
                <li><a href="#" className="hover:text-foreground">New Releases</a></li>
                <li><a href="#" className="hover:text-foreground">Schedule</a></li>
                <li><a href="#" className="hover:text-foreground">Genres</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium mb-4">Legal</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><a href="#" className="hover:text-foreground">Terms of Service</a></li>
                <li><a href="#" className="hover:text-foreground">Privacy Policy</a></li>
                <li><a href="#" className="hover:text-foreground">DMCA</a></li>
                <li><a href="#" className="hover:text-foreground">Contact</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium mb-4">Connect</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><a href="#" className="hover:text-foreground">Discord</a></li>
                <li><a href="#" className="hover:text-foreground">Twitter</a></li>
                <li><a href="#" className="hover:text-foreground">Reddit</a></li>
                <li><a href="#" className="hover:text-foreground">GitHub</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t mt-8 pt-8 text-center text-sm text-muted-foreground">
            <p>© 2024 HiAnime. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}