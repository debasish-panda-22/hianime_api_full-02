"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import { 
  Play, Plus, Star, Clock, Calendar, 
  Loader2, ArrowLeft, Heart, Share2,
  Download, Info, List
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useAnimeDetails, useEpisodes } from "@/hooks/useAnimeData";
import { AnimeDetails, Episode } from "@/lib/api";

const EpisodeCard = ({ episode, animeId }: { episode: Episode; animeId: string }) => {
  return (
    <Card className="hover:shadow-md transition-shadow cursor-pointer">
      <CardContent className="p-4">
        <div className="flex items-center space-x-4">
          <div className="flex-shrink-0">
            <div className="w-16 h-16 bg-gradient-to-br from-primary/20 to-primary/5 rounded flex items-center justify-center">
              <span className="font-semibold text-primary">{episode.number}</span>
            </div>
          </div>
          <div className="flex-1">
            <h4 className="font-medium">{episode.title || `Episode ${episode.number}`}</h4>
            <div className="flex items-center space-x-2 text-sm text-muted-foreground">
              {episode.duration && <span>{episode.duration}</span>}
              {episode.fillers && <Badge variant="outline" className="text-xs">Filler</Badge>}
            </div>
            <div className="flex items-center space-x-2 mt-1">
              {episode.sub && <Badge variant="secondary" className="text-xs">SUB</Badge>}
              {episode.dub && <Badge variant="secondary" className="text-xs">DUB</Badge>}
            </div>
          </div>
          <Button size="sm">
            <Play className="h-4 w-4" />
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

export default function AnimeDetailPage() {
  const params = useParams();
  const router = useRouter();
  const animeId = params.id as string;
  
  const { data: anime, loading: animeLoading, error: animeError } = useAnimeDetails(animeId);
  const { data: episodes, loading: episodesLoading } = useEpisodes(animeId);
  
  const [selectedTab, setSelectedTab] = useState("overview");

  if (animeLoading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    );
  }

  if (animeError || !anime) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-xl font-semibold mb-2">Error loading anime</h2>
          <p className="text-muted-foreground mb-4">{animeError || 'Anime not found'}</p>
          <Button onClick={() => router.back()}>
            <ArrowLeft className="mr-2 h-4 w-4" />
            Go Back
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Back Button */}
      <div className="container mx-auto px-4 py-4">
        <Button 
          variant="ghost" 
          onClick={() => router.back()}
          className="mb-4"
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back
        </Button>
      </div>

      {/* Hero Section */}
      <section className="relative">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Poster */}
            <div className="lg:col-span-1">
              <div className="sticky top-24">
                <div className="aspect-[2/3] w-full max-w-md mx-auto rounded-lg overflow-hidden shadow-lg">
                  {anime.poster ? (
                    <img 
                      src={anime.poster} 
                      alt={anime.title}
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <div className="w-full h-full bg-gradient-to-br from-primary/20 to-primary/5 flex items-center justify-center">
                      <div className="text-center text-muted-foreground">
                        <div className="text-6xl mb-2">🎬</div>
                        <p>Anime Cover</p>
                      </div>
                    </div>
                  )}
                </div>
                
                {/* Action Buttons */}
                <div className="flex space-x-2 mt-4">
                  <Button size="lg" className="flex-1">
                    <Play className="mr-2 h-4 w-4" />
                    Watch Now
                  </Button>
                  <Button size="lg" variant="outline">
                    <Plus className="h-4 w-4" />
                  </Button>
                  <Button size="lg" variant="outline">
                    <Heart className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </div>

            {/* Info */}
            <div className="lg:col-span-2 space-y-6">
              <div>
                <h1 className="text-4xl font-bold mb-2">{anime.title}</h1>
                {anime.alternativeTitle && (
                  <p className="text-xl text-muted-foreground mb-4">{anime.alternativeTitle}</p>
                )}
                
                {/* Metadata */}
                <div className="flex flex-wrap items-center gap-4 mb-6">
                  <div className="flex items-center space-x-1">
                    <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                    <span className="font-medium">{anime.rating || 'N/A'}</span>
                  </div>
                  <Badge variant="outline">{anime.type}</Badge>
                  <Badge variant="outline">{anime.status}</Badge>
                  <div className="flex items-center space-x-1 text-muted-foreground">
                    <Clock className="h-4 w-4" />
                    <span>{anime.duration}</span>
                  </div>
                  <div className="flex items-center space-x-1 text-muted-foreground">
                    <Calendar className="h-4 w-4" />
                    <span>{anime.releaseDate}</span>
                  </div>
                  {anime.episodes && (
                    <Badge variant="secondary">
                      {anime.episodes.eps} Episodes
                    </Badge>
                  )}
                </div>

                {/* Genres */}
                <div className="flex flex-wrap gap-2 mb-6">
                  {anime.genres.map((genre) => (
                    <Badge key={genre} variant="outline">
                      {genre}
                    </Badge>
                  ))}
                </div>

                {/* Synopsis */}
                <div className="mb-6">
                  <h3 className="text-lg font-semibold mb-2">Synopsis</h3>
                  <p className="text-muted-foreground leading-relaxed">
                    {anime.synopsis}
                  </p>
                </div>

                {/* External Links */}
                {(anime.malId || anime.anilistId) && (
                  <div className="flex items-center space-x-4 text-sm">
                    {anime.malId && (
                      <a
                        href={`https://myanimelist.net/anime/${anime.malId}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-primary hover:underline"
                      >
                        MyAnimeList
                      </a>
                    )}
                    {anime.anilistId && (
                      <a
                        href={`https://anilist.co/anime/${anime.anilistId}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-primary hover:underline"
                      >
                        AniList
                      </a>
                    )}
                  </div>
                )}
              </div>

              {/* Tabs */}
              <Tabs value={selectedTab} onValueChange={setSelectedTab}>
                <TabsList className="grid w-full grid-cols-3">
                  <TabsTrigger value="overview">Overview</TabsTrigger>
                  <TabsTrigger value="episodes">
                    Episodes
                    {anime.episodes && (
                      <Badge variant="secondary" className="ml-2 text-xs">
                        {anime.episodes.eps}
                      </Badge>
                    )}
                  </TabsTrigger>
                  <TabsTrigger value="related">Related</TabsTrigger>
                </TabsList>

                <TabsContent value="overview" className="mt-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <Card>
                      <CardHeader>
                        <CardTitle className="text-lg">Information</CardTitle>
                      </CardHeader>
                      <CardContent className="space-y-3">
                        <div className="flex justify-between">
                          <span className="text-muted-foreground">Type:</span>
                          <span>{anime.type}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-muted-foreground">Status:</span>
                          <span>{anime.status}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-muted-foreground">Duration:</span>
                          <span>{anime.duration}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-muted-foreground">Quality:</span>
                          <span>{anime.quality}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-muted-foreground">Release Date:</span>
                          <span>{anime.releaseDate}</span>
                        </div>
                        {anime.episodes && (
                          <>
                            <div className="flex justify-between">
                              <span className="text-muted-foreground">Episodes:</span>
                              <span>{anime.episodes.eps}</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-muted-foreground">Subbed:</span>
                              <span>{anime.episodes.sub || 'N/A'}</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-muted-foreground">Dubbed:</span>
                              <span>{anime.episodes.dub || 'N/A'}</span>
                            </div>
                          </>
                        )}
                      </CardContent>
                    </Card>

                    <Card>
                      <CardHeader>
                        <CardTitle className="text-lg">Statistics</CardTitle>
                      </CardHeader>
                      <CardContent className="space-y-3">
                        <div className="flex justify-between">
                          <span className="text-muted-foreground">Rating:</span>
                          <div className="flex items-center space-x-1">
                            <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                            <span>{anime.rating || 'N/A'}</span>
                          </div>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-muted-foreground">MAL ID:</span>
                          <span>{anime.malId || 'N/A'}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-muted-foreground">AniList ID:</span>
                          <span>{anime.anilistId || 'N/A'}</span>
                        </div>
                      </CardContent>
                    </Card>
                  </div>
                </TabsContent>

                <TabsContent value="episodes" className="mt-6">
                  {episodesLoading ? (
                    <div className="flex items-center justify-center py-12">
                      <Loader2 className="h-8 w-8 animate-spin" />
                    </div>
                  ) : episodes && episodes.length > 0 ? (
                    <ScrollArea className="h-[600px]">
                      <div className="space-y-3">
                        {episodes.map((episode) => (
                          <EpisodeCard 
                            key={episode.id} 
                            episode={episode} 
                            animeId={animeId}
                          />
                        ))}
                      </div>
                    </ScrollArea>
                  ) : (
                    <div className="text-center py-12 text-muted-foreground">
                      No episodes available
                    </div>
                  )}
                </TabsContent>

                <TabsContent value="related" className="mt-6">
                  <div className="text-center py-12 text-muted-foreground">
                    <Info className="h-12 w-12 mx-auto mb-4 opacity-50" />
                    <p>Related anime information will be available soon.</p>
                  </div>
                </TabsContent>
              </Tabs>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}