#!/usr/bin/env python3
"""
debug_episodes_stream_debug.py

1) Calls the /search, /anime/<id>/, /episodes/<id>/ endpoints and saves outputs.
2) If episodes list is empty, tries to fetch a few candidate provider page URLs
   built from ANIME_API_PROVIDERS env var or .env file.
3) Saves everything to test_results_verbose.txt for sharing.
"""

import os, sys, json, requests, time, re
from urllib.parse import urljoin

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000/api/v1")
OUTPUT = "test_results_verbose.txt"
PROVIDER = os.getenv("ANIME_API_PROVIDERS", None)

# Try to load .env in project root if provider not in env
if not PROVIDER:
    env_path = os.path.join(os.getcwd(), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                m = re.match(r'\s*ANIME_API_PROVIDERS\s*=\s*(.+)\s*', line)
                if m:
                    PROVIDER = m.group(1).strip().strip('"').strip("'")
                    break

def save_section(title, data):
    with open(OUTPUT, "a", encoding="utf-8") as fh:
        fh.write("\n" + "="*80 + "\n")
        fh.write(title+"\n")
        fh.write("="*80 + "\n")
        if isinstance(data, (dict, list)):
            fh.write(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            fh.write(str(data))
        fh.write("\n\n")

def safe_get(url, headers=None, timeout=15):
    try:
        r = requests.get(url, headers=headers, timeout=timeout)
        return r
    except Exception as e:
        return e

def main():
    if os.path.exists(OUTPUT):
        os.remove(OUTPUT)

    print("Debugging HiAnime API... results ->", OUTPUT)
    # 1) Search (naruto)
    s = safe_get(f"{BASE_URL}/search/?keyword=naruto")
    save_section("Search (naruto) raw", s.text if hasattr(s, "text") else str(s))
    try:
        search_json = s.json() if hasattr(s, "json") else {}
    except Exception:
        search_json = {}
    save_section("Search (naruto) parsed", search_json)

    # try to extract anime_id from search response
    anime_id = None
    try:
        # common path: data->response (based on earlier script)
        anime_list = search_json.get("data", {}).get("response") or search_json.get("data") or []
        if isinstance(anime_list, dict):
            # maybe single object
            anime_list = [anime_list]
        if anime_list:
            anime_id = anime_list[0].get("id") or anime_list[0].get("slug") or anime_list[0].get("anime_id")
    except Exception:
        anime_id = None

    save_section("Extracted anime_id (attempt)", anime_id)

    if not anime_id:
        print("Could not auto-extract anime_id from search. Please provide anime_id manually and re-run:")
        print("Example: python3 debug_episodes_stream_debug.py <anime_id>")
        if len(sys.argv) > 1:
            anime_id = sys.argv[1]
            print("Using anime_id from argv:", anime_id)
        else:
            return

    # 2) Anime details
    details = safe_get(f"{BASE_URL}/anime/{anime_id}/")
    save_section(f"Anime Details /anime/{anime_id}/ raw", details.text if hasattr(details, "text") else str(details))
    try:
        details_json = details.json()
    except Exception:
        details_json = {}
    save_section(f"Anime Details parsed", details_json)

    # 3) Episodes
    episodes = safe_get(f"{BASE_URL}/episodes/{anime_id}/")
    save_section(f"Episodes /episodes/{anime_id}/ raw", episodes.text if hasattr(episodes, "text") else str(episodes))
    try:
        episodes_json = episodes.json()
    except Exception:
        episodes_json = {}
    save_section("Episodes parsed", episodes_json)

    # If episodes empty, attempt to fetch provider page(s)
    ep_data = episodes_json.get("data") if isinstance(episodes_json, dict) else None
    if not ep_data:
        save_section("NOTE", "Episode data is empty from API; attempting to fetch provider pages (best-effort).")
        if PROVIDER:
            save_section("Provider base found", PROVIDER)
            # try common path patterns used by scrapers — try a few guesses
            candidates = [
                f"/anime/{anime_id}",
                f"/category/{anime_id}",
                f"/anime-details/{anime_id}",
                f"/{anime_id}",  # sometimes the slug alone works
            ]
            for c in candidates:
                url = urljoin(PROVIDER.rstrip('/')+'/', c.lstrip('/'))
                r = safe_get(url)
                save_section(f"Provider fetch: {url}", r.text if hasattr(r, "text") else str(r))
                time.sleep(0.5)
        else:
            save_section("Provider base", "ANIME_API_PROVIDERS not set (env or .env). Cannot auto-fetch provider pages.")

    # 4) Servers & Streaming attempts (best-effort)
    # attempt to get an episode id from episodes_json list
    episode_id = None
    try:
        if isinstance(episodes_json.get("data"), list) and episodes_json.get("data"):
            ep0 = episodes_json["data"][0]
            episode_id = ep0.get("id") or ep0.get("episode_id") or ep0.get("url")
    except Exception:
        episode_id = None
    save_section("Extracted episode_id (attempt)", episode_id)

    if episode_id:
        srv = safe_get(f"{BASE_URL}/servers/?id={episode_id}")
        save_section(f"Servers ?id={episode_id}", srv.text if hasattr(srv, "text") else str(srv))
        try:
            sjson = srv.json()
        except Exception:
            sjson = {}
        save_section("Servers parsed", sjson)
        if isinstance(sjson, dict) and sjson.get("data"):
            # pick first server name from sub/dub
            servers = sjson["data"].get("sub") or sjson["data"].get("dub") or []
            if servers:
                server_name = servers[0].get("name")
                stream = safe_get(f"{BASE_URL}/stream/?id={episode_id}&server={server_name}&type=sub")
                save_section(f"Stream ?id={episode_id}&server={server_name}&type=sub", stream.text if hasattr(stream,"text") else str(stream))
    else:
        save_section("No episode_id", "No episode_id extracted; cannot test servers/stream automatically.")

    print("Debugging complete. See", OUTPUT, "and share it with me.")
    print("If you want, run with explicit anime_id: python3 debug_episodes_stream_debug.py <anime_id>")

if __name__ == "__main__":
    main()
