"use strict";
// Mock API data for testing the frontend without a running backend
Object.defineProperty(exports, "__esModule", { value: true });
exports.mockAnimeApi = void 0;
// Mock data
const mockAnime = [
    {
        id: "one-piece-100",
        title: "One Piece",
        alternativeTitle: "ワンピース",
        poster: "https://cdn.noitatnemucod.net/thumbnail/300x400/100/db8603d2f4fa78e1c42f6cf829030a18.jpg",
        type: "TV",
        duration: "24m",
        episodes: {
            sub: 1000,
            dub: 1000,
            eps: 1000
        },
        rating: 8.5,
        status: "Airing",
        genres: ["Action", "Adventure", "Comedy", "Drama", "Shounen"],
        description: "Gold Roger was known as the \"Pirate King,\" the strongest and most infamous being to have sailed the Grand Line."
    },
    {
        id: "naruto-100",
        title: "Naruto",
        alternativeTitle: "ナルト",
        poster: "https://cdn.noitatnemucod.net/thumbnail/300x400/100/32c83e2ad4a43229996356840db3982c.jpg",
        type: "TV",
        duration: "23m",
        episodes: {
            sub: 220,
            dub: 220,
            eps: 220
        },
        rating: 8.3,
        status: "Completed",
        genres: ["Action", "Adventure", "Martial Arts", "Shounen", "Super Power"],
        description: "Naruto Uzumaki is a hyperactive and knuckle-headed ninja still living in Konohagakure."
    },
    {
        id: "attack-on-titan-100",
        title: "Attack on Titan",
        alternativeTitle: "進撃の巨人",
        poster: "https://cdn.noitatnemucod.net/thumbnail/300x400/100/da3a3d57e29aa0dba87cd6e1596b78e9.jpg",
        type: "TV",
        duration: "24m",
        episodes: {
            sub: 75,
            dub: 75,
            eps: 75
        },
        rating: 9.0,
        status: "Completed",
        genres: ["Action", "Drama", "Fantasy", "Military", "Mystery"],
        description: "Centuries ago, mankind was slaughtered to near extinction by monstrous humanoid creatures called Titans."
    },
    {
        id: "demon-slayer-100",
        title: "Demon Slayer",
        alternativeTitle: "鬼滅の刃",
        poster: "https://cdn.noitatnemucod.net/thumbnail/300x400/100/fd414879634ea83ad2c4fc1c33e8ac43.jpg",
        type: "TV",
        duration: "24m",
        episodes: {
            sub: 26,
            dub: 26,
            eps: 26
        },
        rating: 8.7,
        status: "Completed",
        genres: ["Action", "Historical", "Shounen", "Supernatural"],
        description: "Tanjirou Kamado lives with his impoverished family on a remote mountain."
    },
    {
        id: "jujutsu-kaisen-100",
        title: "Jujutsu Kaisen",
        alternativeTitle: "呪術廻戦",
        poster: "https://cdn.noitatnemucod.net/thumbnail/300x400/100/73d003618cd260df44e93a5baf9acb56.jpg",
        type: "TV",
        duration: "24m",
        episodes: {
            sub: 24,
            dub: 24,
            eps: 24
        },
        rating: 8.5,
        status: "Completed",
        genres: ["Action", "School", "Shounen", "Supernatural"],
        description: "Idly indulging in baseless paranormal activities with the Occult Club."
    }
];
const mockEpisodes = [
    {
        id: "one-piece-100-ep1",
        number: 1,
        title: "I'm Luffy! The Man Who's Gonna Be King of the Pirates!",
        duration: "24m",
        sub: true,
        dub: true
    },
    {
        id: "one-piece-100-ep2",
        number: 2,
        title: "Enter the Great Swordsman! Pirate Hunter, Roronoa Zoro!",
        duration: "24m",
        sub: true,
        dub: true
    },
    {
        id: "one-piece-100-ep3",
        number: 3,
        title: "Morgan versus Luffy! Who's This Mysterious Pretty Girl?",
        duration: "24m",
        sub: true,
        dub: true
    }
];
const mockGenres = [
    "Action", "Adventure", "Comedy", "Drama", "Fantasy", "Horror", "Mystery",
    "Romance", "Sci-Fi", "Slice of Life", "Sports", "Supernatural", "Thriller"
];
// Mock API functions
exports.mockAnimeApi = {
    // Get homepage data
    getHomepage: async () => {
        await new Promise(resolve => setTimeout(resolve, 500)); // Simulate API delay
        return {
            success: true,
            data: {
                spotlight: mockAnime.slice(0, 2),
                trending: mockAnime.slice(0, 3),
                topAiring: mockAnime.slice(0, 4),
                mostPopular: mockAnime,
                mostFavorite: mockAnime.slice(0, 3),
                latestEpisode: mockAnime.slice(0, 4),
                topUpcoming: mockAnime.slice(0, 2),
                genres: mockGenres
            }
        };
    },
    // Search anime
    searchAnime: async (keyword, page = 1) => {
        await new Promise(resolve => setTimeout(resolve, 300));
        const filtered = mockAnime.filter(anime => {
            var _a;
            return anime.title.toLowerCase().includes(keyword.toLowerCase()) ||
                ((_a = anime.alternativeTitle) === null || _a === void 0 ? void 0 : _a.toLowerCase().includes(keyword.toLowerCase()));
        });
        return {
            success: true,
            data: {
                pageInfo: {
                    totalPages: Math.max(1, Math.ceil(filtered.length / 10)),
                    currentPage: page,
                    hasNextPage: page < Math.ceil(filtered.length / 10)
                },
                response: filtered
            }
        };
    },
    // Get search suggestions
    getSuggestions: async (keyword) => {
        await new Promise(resolve => setTimeout(resolve, 200));
        const suggestions = mockAnime
            .filter(anime => anime.title.toLowerCase().includes(keyword.toLowerCase()))
            .map(anime => anime.title)
            .slice(0, 5);
        return {
            success: true,
            data: suggestions
        };
    },
    // Get anime details
    getAnimeDetails: async (animeId) => {
        await new Promise(resolve => setTimeout(resolve, 400));
        const anime = mockAnime.find(a => a.id === animeId);
        if (!anime) {
            return { success: false, message: "Anime not found" };
        }
        return {
            success: true,
            data: {
                ...anime,
                quality: "HD",
                releaseDate: "2020",
                status: "Airing",
                synopsis: anime.description || "No synopsis available.",
                genres: anime.genres || [],
                episodesList: mockEpisodes
            }
        };
    },
    // Get anime list by category
    getAnimeList: async (query, category, page = 1) => {
        await new Promise(resolve => setTimeout(resolve, 300));
        let filtered = [...mockAnime];
        if (query === "most-popular") {
            filtered = mockAnime.sort((a, b) => (b.rating || 0) - (a.rating || 0));
        }
        else if (query === "top-airing") {
            filtered = mockAnime.filter(a => a.status === "Airing");
        }
        return {
            success: true,
            data: {
                pageInfo: {
                    totalPages: Math.max(1, Math.ceil(filtered.length / 10)),
                    currentPage: page,
                    hasNextPage: page < Math.ceil(filtered.length / 10)
                },
                response: filtered
            }
        };
    },
    // Get episodes
    getEpisodes: async (animeId) => {
        await new Promise(resolve => setTimeout(resolve, 300));
        return {
            success: true,
            data: mockEpisodes
        };
    },
    // Get genres
    getGenres: async () => {
        await new Promise(resolve => setTimeout(resolve, 200));
        return {
            success: true,
            data: mockGenres
        };
    }
};
