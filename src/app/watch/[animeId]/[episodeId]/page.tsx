"use client";

import { useState, useEffect, useRef } from "react";
import { useParams, useRouter } from "next/navigation";
import { 
  Play, Pause, Volume2, VolumeX, Maximize, 
  Settings, ArrowLeft, Loader2, AlertCircle,
  SkipBack, SkipForward, Monitor, Smartphone
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useAnimeDetails, useEpisodes } from "@/hooks/useAnimeData";
import { animeApi } from "@/lib/api";

interface ServerOption {
  name: string;
  serverId: string;
}

interface VideoSource {
  file: string;
  type: string;
  label?: string;
}

export default function WatchPage() {
  const params = useParams();
  const router = useRouter();
  const animeId = params.animeId as string;
  const episodeId = params.episodeId as string;
  
  const { data: anime, loading: animeLoading } = useAnimeDetails(animeId);
  const { data: episodes, loading: episodesLoading } = useEpisodes(animeId);
  
  const [servers, setServers] = useState<ServerOption[]>([]);
  const [selectedServer, setSelectedServer] = useState<string>("");
  const [videoSources, setVideoSources] = useState<VideoSource[]>([]);
  const [selectedSource, setSelectedSource] = useState<VideoSource | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isMuted, setIsMuted] = useState(false);
  const [volume, setVolume] = useState(1);
  const [playbackRate, setPlaybackRate] = useState(1);
  const [quality, setQuality] = useState<string>("auto");
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [showControls, setShowControls] = useState(true);

  const videoRef = useRef<HTMLVideoElement>(null);

  // Load servers and video sources
  useEffect(() => {
    const loadVideoData = async () => {
      try {
        setLoading(true);
        setError(null);

        // Get available servers
        const serversResponse = await animeApi.getServers(episodeId);
        if (serversResponse.success && serversResponse.data) {
          setServers(serversResponse.data);
          if (serversResponse.data.length > 0) {
            setSelectedServer(serversResponse.data[0].serverId);
          }
        }

        // Get streaming links for the first server
        if (serversResponse.data && serversResponse.data.length > 0) {
          const streamResponse = await animeApi.getStreamingLinks(
            episodeId, 
            serversResponse.data[0].serverId, 
            'sub'
          );
          
          if (streamResponse.success && streamResponse.data) {
            setVideoSources(streamResponse.data.sources);
            if (streamResponse.data.sources.length > 0) {
              setSelectedSource(streamResponse.data.sources[0]);
            }
          }
        }
      } catch (err) {
        console.error('Error loading video data:', err);
        setError('Failed to load video. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    loadVideoData();
  }, [episodeId]);

  // Handle server change
  const handleServerChange = async (serverId: string) => {
    try {
      setSelectedServer(serverId);
      const streamResponse = await animeApi.getStreamingLinks(episodeId, serverId, 'sub');
      
      if (streamResponse.success && streamResponse.data) {
        setVideoSources(streamResponse.data.sources);
        if (streamResponse.data.sources.length > 0) {
          setSelectedSource(streamResponse.data.sources[0]);
        }
      }
    } catch (err) {
      console.error('Error changing server:', err);
      setError('Failed to change server. Please try again.');
    }
  };

  // Video event handlers
  const handlePlayPause = () => {
    if (videoRef.current) {
      if (videoRef.current.paused) {
        videoRef.current.play();
        setIsPlaying(true);
      } else {
        videoRef.current.pause();
        setIsPlaying(false);
      }
    }
  };

  const handleTimeUpdate = () => {
    if (videoRef.current) {
      setCurrentTime(videoRef.current.currentTime);
    }
  };

  const handleLoadedMetadata = () => {
    if (videoRef.current) {
      setDuration(videoRef.current.duration);
    }
  };

  const handleVolumeChange = (newVolume: number) => {
    setVolume(newVolume);
    setIsMuted(newVolume === 0);
    if (videoRef.current) {
      videoRef.current.volume = newVolume;
    }
  };

  const handleMuteToggle = () => {
    setIsMuted(!isMuted);
    if (videoRef.current) {
      videoRef.current.muted = !isMuted;
    }
  };

  const handleSeek = (time: number) => {
    if (videoRef.current) {
      videoRef.current.currentTime = time;
      setCurrentTime(time);
    }
  };

  const handlePlaybackRateChange = (rate: number) => {
    setPlaybackRate(rate);
    if (videoRef.current) {
      videoRef.current.playbackRate = rate;
    }
  };

  const formatTime = (time: number) => {
    const hours = Math.floor(time / 3600);
    const minutes = Math.floor((time % 3600) / 60);
    const seconds = Math.floor(time % 60);
    
    if (hours > 0) {
      return `${hours}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  // Auto-hide controls
  useEffect(() => {
    let timeout: NodeJS.Timeout;
    
    if (isPlaying && showControls) {
      timeout = setTimeout(() => {
        setShowControls(false);
      }, 3000);
    }

    return () => {
      if (timeout) {
        clearTimeout(timeout);
      }
    };
  }, [isPlaying, showControls]);

  if (loading || animeLoading || episodesLoading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="h-12 w-12 animate-spin mx-auto mb-4" />
          <p className="text-muted-foreground">Loading video...</p>
        </div>
      </div>
    );
  }

  if (error || !anime || !episodes) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center max-w-md">
          <AlertCircle className="h-12 w-12 text-destructive mx-auto mb-4" />
          <h2 className="text-xl font-semibold mb-2">Error Loading Video</h2>
          <p className="text-muted-foreground mb-4">{error || 'Failed to load video content'}</p>
          <div className="space-y-2">
            <Button onClick={() => router.back()} className="w-full">
              <ArrowLeft className="mr-2 h-4 w-4" />
              Go Back
            </Button>
            <Button onClick={() => window.location.reload()} variant="outline" className="w-full">
              Try Again
            </Button>
          </div>
        </div>
      </div>
    );
  }

  const currentEpisode = episodes.find(ep => ep.id === episodeId);
  const currentEpisodeIndex = episodes.findIndex(ep => ep.id === episodeId);

  const handlePreviousEpisode = () => {
    if (currentEpisodeIndex > 0) {
      const prevEpisode = episodes[currentEpisodeIndex - 1];
      router.push(`/watch/${animeId}/${prevEpisode.id}`);
    }
  };

  const handleNextEpisode = () => {
    if (currentEpisodeIndex < episodes.length - 1) {
      const nextEpisode = episodes[currentEpisodeIndex + 1];
      router.push(`/watch/${animeId}/${nextEpisode.id}`);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Video Player */}
      <div className="relative bg-black aspect-video">
        {selectedSource ? (
          <video
            ref={videoRef}
            src={selectedSource.file}
            className="w-full h-full"
            onPlay={() => setIsPlaying(true)}
            onPause={() => setIsPlaying(false)}
            onTimeUpdate={handleTimeUpdate}
            onLoadedMetadata={handleLoadedMetadata}
            onEnded={() => setIsPlaying(false)}
            onClick={() => setShowControls(!showControls)}
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center">
            <div className="text-center text-white">
              <AlertCircle className="h-12 w-12 mx-auto mb-4" />
              <p>No video source available</p>
            </div>
          </div>
        )}

        {/* Video Controls Overlay */}
        {showControls && (
          <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-black/80">
            {/* Top Controls */}
            <div className="absolute top-0 left-0 right-0 p-4 flex items-center justify-between">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => router.back()}
                className="text-white hover:text-white hover:bg-white/20"
              >
                <ArrowLeft className="h-4 w-4 mr-2" />
                Back
              </Button>
              
              <div className="flex items-center space-x-2">
                <Badge variant="secondary" className="text-white bg-white/20">
                  {currentEpisode?.title || `Episode ${currentEpisode?.number}`}
                </Badge>
              </div>
            </div>

            {/* Center Play/Pause */}
            <div className="absolute inset-0 flex items-center justify-center">
              <Button
                size="lg"
                variant="ghost"
                onClick={handlePlayPause}
                className="text-white hover:text-white hover:bg-white/20 h-16 w-16 rounded-full"
              >
                {isPlaying ? (
                  <Pause className="h-8 w-8" />
                ) : (
                  <Play className="h-8 w-8" />
                )}
              </Button>
            </div>

            {/* Bottom Controls */}
            <div className="absolute bottom-0 left-0 right-0 p-4">
              {/* Progress Bar */}
              <div className="mb-4">
                <div className="flex items-center space-x-2 text-white text-sm">
                  <span>{formatTime(currentTime)}</span>
                  <div className="flex-1 bg-white/30 rounded-full h-1 cursor-pointer" onClick={(e) => {
                    const rect = e.currentTarget.getBoundingClientRect();
                    const percent = (e.clientX - rect.left) / rect.width;
                    handleSeek(percent * duration);
                  }}>
                    <div 
                      className="bg-primary h-full rounded-full transition-all duration-100"
                      style={{ width: `${(currentTime / duration) * 100}%` }}
                    />
                  </div>
                  <span>{formatTime(duration)}</span>
                </div>
              </div>

              {/* Control Buttons */}
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={handlePreviousEpisode}
                    disabled={currentEpisodeIndex <= 0}
                    className="text-white hover:text-white hover:bg-white/20"
                  >
                    <SkipBack className="h-4 w-4" />
                  </Button>
                  
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={handlePlayPause}
                    className="text-white hover:text-white hover:bg-white/20"
                  >
                    {isPlaying ? (
                      <Pause className="h-4 w-4" />
                    ) : (
                      <Play className="h-4 w-4" />
                    )}
                  </Button>
                  
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={handleNextEpisode}
                    disabled={currentEpisodeIndex >= episodes.length - 1}
                    className="text-white hover:text-white hover:bg-white/20"
                  >
                    <SkipForward className="h-4 w-4" />
                  </Button>

                  <div className="flex items-center space-x-2 ml-4">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={handleMuteToggle}
                      className="text-white hover:text-white hover:bg-white/20"
                    >
                      {isMuted ? (
                        <VolumeX className="h-4 w-4" />
                      ) : (
                        <Volume2 className="h-4 w-4" />
                      )}
                    </Button>
                    <input
                      type="range"
                      min="0"
                      max="1"
                      step="0.1"
                      value={volume}
                      onChange={(e) => handleVolumeChange(parseFloat(e.target.value))}
                      className="w-20 accent-primary"
                    />
                  </div>
                </div>

                <div className="flex items-center space-x-2">
                  <Select value={selectedServer} onValueChange={handleServerChange}>
                    <SelectTrigger className="w-32 bg-white/20 text-white border-white/30">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {servers.map((server) => (
                        <SelectItem key={server.serverId} value={server.serverId}>
                          {server.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>

                  <Select value={quality} onValueChange={setQuality}>
                    <SelectTrigger className="w-24 bg-white/20 text-white border-white/30">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="auto">Auto</SelectItem>
                      {videoSources.map((source, index) => (
                        <SelectItem key={index} value={source.label || `${index}`}>
                          {source.label || `Source ${index + 1}`}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>

                  <Select value={playbackRate.toString()} onValueChange={(value) => handlePlaybackRateChange(parseFloat(value))}>
                    <SelectTrigger className="w-20 bg-white/20 text-white border-white/30">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="0.5">0.5x</SelectItem>
                      <SelectItem value="0.75">0.75x</SelectItem>
                      <SelectItem value="1">1x</SelectItem>
                      <SelectItem value="1.25">1.25x</SelectItem>
                      <SelectItem value="1.5">1.5x</SelectItem>
                      <SelectItem value="2">2x</SelectItem>
                    </SelectContent>
                  </Select>

                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => document.documentElement.requestFullscreen()}
                    className="text-white hover:text-white hover:bg-white/20"
                  >
                    <Maximize className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Episode List */}
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Anime Info */}
          <div className="lg:col-span-1">
            <Card>
              <CardContent className="p-6">
                <div className="space-y-4">
                  <div>
                    <h2 className="text-xl font-bold">{anime.title}</h2>
                    {anime.alternativeTitle && (
                      <p className="text-sm text-muted-foreground">{anime.alternativeTitle}</p>
                    )}
                  </div>
                  
                  <div className="aspect-[2/3] w-full max-w-xs mx-auto rounded-lg overflow-hidden">
                    {anime.poster ? (
                      <img 
                        src={anime.poster} 
                        alt={anime.title}
                        className="w-full h-full object-cover"
                      />
                    ) : (
                      <div className="w-full h-full bg-gradient-to-br from-primary/20 to-primary/5 flex items-center justify-center">
                        <div className="text-center text-muted-foreground">
                          <div className="text-4xl mb-2">🎬</div>
                          <p>Anime Cover</p>
                        </div>
                      </div>
                    )}
                  </div>

                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Type:</span>
                      <span>{anime.type}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Status:</span>
                      <span>{anime.status}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Episodes:</span>
                      <span>{anime.episodes?.eps || 'N/A'}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Duration:</span>
                      <span>{anime.duration}</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Episode List */}
          <div className="lg:col-span-3">
            <Card>
              <CardContent className="p-6">
                <h3 className="text-lg font-semibold mb-4">Episode List</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-h-96 overflow-y-auto">
                  {episodes.map((episode) => (
                    <div
                      key={episode.id}
                      className={`p-3 border rounded-lg cursor-pointer transition-colors ${
                        episode.id === episodeId
                          ? 'bg-primary text-primary-foreground border-primary'
                          : 'bg-muted/50 hover:bg-muted border-border'
                      }`}
                      onClick={() => router.push(`/watch/${animeId}/${episode.id}`)}
                    >
                      <div className="flex items-center justify-between">
                        <div>
                          <h4 className="font-medium text-sm">
                            {episode.title || `Episode ${episode.number}`}
                          </h4>
                          <div className="flex items-center space-x-2 mt-1">
                            {episode.sub && <Badge variant="secondary" className="text-xs">SUB</Badge>}
                            {episode.dub && <Badge variant="secondary" className="text-xs">DUB</Badge>}
                            {episode.duration && (
                              <span className="text-xs text-muted-foreground">{episode.duration}</span>
                            )}
                          </div>
                        </div>
                        {episode.id === episodeId && (
                          <div className="w-2 h-2 bg-current rounded-full"></div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}