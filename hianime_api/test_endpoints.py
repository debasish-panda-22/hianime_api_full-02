#!/usr/bin/env python3
"""
Test all HiAnime Django API endpoints and save results to test_results.txt
"""

import requests
import json
import os

BASE_URL = "http://localhost:8000/api/v1"
OUTPUT_FILE = "test_results.txt"


def write_output(title, response):
    """Helper to write sectioned output to file"""
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write("\n" + "=" * 80 + "\n")
        f.write(f"### {title}\n")
        f.write("=" * 80 + "\n")
        try:
            f.write(f"Status: {response.status_code}\n")
            data = response.json()
            f.write(json.dumps(data, indent=2, ensure_ascii=False))
        except Exception:
            f.write(response.text)


def main():
    # Reset file
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    print(f"🧪 Testing HiAnime API at {BASE_URL} ... results will be saved to {OUTPUT_FILE}")

    # 1. Root
    write_output("Root", requests.get(f"{BASE_URL}/"))

    # 2. Homepage
    write_output("Homepage", requests.get(f"{BASE_URL}/home/"))

    # 3. Search
    search_resp = requests.get(f"{BASE_URL}/search/?keyword=naruto")
    write_output("Search (naruto)", search_resp)

    # Extract anime_id from search for next tests
    anime_id = None
    try:
        results = search_resp.json().get("data", {}).get("response", [])
        if results:
            anime_id = results[0].get("id")
    except Exception:
        pass

    if anime_id:
        # 4. Anime Details
        write_output("Anime Details", requests.get(f"{BASE_URL}/anime/{anime_id}/"))

        # 5. Episodes
        episodes_resp = requests.get(f"{BASE_URL}/episodes/{anime_id}/")
        write_output("Episodes", episodes_resp)

        # Extract an episode_id
        episode_id = None
        try:
            eps = episodes_resp.json().get("data", [])
            if eps:
                episode_id = eps[0].get("id")
        except Exception:
            pass

        if episode_id:
            # 6. Servers
            servers_resp = requests.get(f"{BASE_URL}/servers/?id={episode_id}")
            write_output("Servers", servers_resp)

            # Extract server name
            server_name = None
            stream_type = "sub"
            try:
                servers_data = servers_resp.json().get("data", {})
                if servers_data.get("sub"):
                    server_name = servers_data["sub"][0].get("name")
            except Exception:
                pass

            if server_name:
                # 7. Stream
                stream_url = f"{BASE_URL}/stream/?id={episode_id}&server={server_name}&type={stream_type}"
                write_output("Stream", requests.get(stream_url))

    # 8. Genres
    write_output("Genres", requests.get(f"{BASE_URL}/genres/"))

    # 9. Anime Lists
    for cat in ["top-airing", "most-popular", "most-favorite", "completed", "recently-added"]:
        write_output(f"Anime List ({cat})", requests.get(f"{BASE_URL}/animes/{cat}/"))

    print(f"✅ Testing complete. Results saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
