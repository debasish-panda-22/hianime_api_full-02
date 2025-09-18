#!/usr/bin/env python3
"""
compact_test_debug.py
Lightweight, shareable summary for debugging HiAnime endpoints.

Creates:
 - test_summary.txt  (concise, human-readable)
 - raw_snippet.html   (first ~2000 chars of any fetched HTML we need)
"""
import os, json, requests, re, time
from urllib.parse import urljoin

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000/api/v1")
OUTPUT = "test_summary.txt"
SNIPPET = "raw_snippet.html"
KEY_SELECTORS = [
    r"\.ssl-item\.ep-item",
    r"#syncData",
    r"\.server-item",
    r"data-id",
    r"data-type",
    r"iframe",
    r"m3u8",
    r"megaplay",
    r"megacloud",
    r"tick-sub",
    r"tick-dub",
]

def write(s):
    with open(OUTPUT, "a", encoding="utf-8") as fh:
        fh.write(s + "\n")

def small_preview(text, n=2000):
    if text is None:
        return "<empty>"
    txt = text if isinstance(text, str) else str(text)
    if len(txt) <= n:
        return txt
    return txt[:n] + "\n\n...TRUNCATED...\n"

def try_json(resp):
    try:
        return resp.json()
    except Exception:
        return None

def check_patterns(text, patterns):
    hits = {}
    for p in patterns:
        try:
            hits[p] = bool(re.search(p, text, re.I | re.M))
        except Exception:
            hits[p] = False
    return hits

def call(url, label):
    try:
        r = requests.get(url, timeout=15)
    except Exception as e:
        return {"ok": False, "error": str(e)}
    return {
        "ok": True,
        "status": r.status_code,
        "len": len(r.content or b""),
        "text": r.text[:20000],  # keep some headroom but not entire body
        "json": try_json(r)
    }

def summarize_response(label, res):
    write("="*70)
    write(f"{label}")
    write("="*70)
    if not res.get("ok"):
        write("ERROR: " + res.get("error", "unknown"))
        return
    write(f"Status: {res['status']}, Response bytes: {res['len']}")
    j = res.get("json")
    if j is not None:
        # JSON summary
        j_small = json.dumps(j, indent=2, ensure_ascii=False)
        write("JSON preview (first ~2000 chars):")
        write(small_preview(j_small, 2000))
    else:
        write("Text/HTML preview (first ~2000 chars):")
        write(small_preview(res.get("text", ""), 2000))
    # pattern checks
    text_for_check = res.get("text", "") or (json.dumps(res.get("json"), ensure_ascii=False) if res.get("json") else "")
    patterns = check_patterns(text_for_check, KEY_SELECTORS)
    write("Pattern checks (presence = True/False):")
    for k,v in patterns.items():
        write(f"  {k} : {v}")

def extract_syncdata_and_small_episodes(html_text):
    """Look for #syncData JSON and pull a small snapshot."""
    try:
        m = re.search(r'<[^>]*id=["\']syncData["\'][^>]*>(.*?)</', html_text, re.I|re.S)
        if not m:
            # try tag with id and text content
            m2 = re.search(r'id=["\']syncData["\'][^>]*>(.*?)</', html_text, re.I|re.S)
            if m2:
                raw = m2.group(1).strip()
            else:
                return None
        else:
            raw = m.group(1).strip()
        # Sometimes raw may be HTML-escaped; try to load JSON
        raw = raw.strip()
        parsed = None
        try:
            parsed = json.loads(raw)
        except Exception:
            # try unescape common entities
            try:
                import html
                un = html.unescape(raw)
                parsed = json.loads(un)
            except Exception:
                parsed = None
        if parsed:
            # produce small snapshot: keys and first few episodes if present
            snap = {"top_keys": list(parsed.keys())[:20]}
            # common keys that might contain episodes lists
            for k in ("episodes","episodesList","epList","data"):
                if k in parsed and isinstance(parsed[k], (list,dict)):
                    if isinstance(parsed[k], list):
                        snap[k] = parsed[k][:10]
                    else:
                        # dict -> show first-level keys and maybe first 10 items if list inside
                        snap[k] = {kk: (parsed[k][kk][:10] if isinstance(parsed[k][kk], list) else str(type(parsed[k][kk])) ) for kk in list(parsed[k].keys())[:20]}
            return snap
    except Exception:
        return None
    return None

def main():
    if os.path.exists(OUTPUT):
        os.remove(OUTPUT)
    if os.path.exists(SNIPPET):
        os.remove(SNIPPET)

    write("Compact HiAnime API debug summary")
    write("BASE_URL: " + BASE_URL)
    write("Timestamp: " + time.strftime("%Y-%m-%d %H:%M:%S"))

    # 1. Root
    r = call(f"{BASE_URL}/", "Root /")
    summarize_response("Root /", r)

    # 2. Home
    r = call(f"{BASE_URL}/home/", "Homepage /home/")
    summarize_response("Homepage /home/", r)

    # 3. Search (naruto)
    search = call(f"{BASE_URL}/search/?keyword=naruto", "Search /search/?keyword=naruto")
    summarize_response("Search (naruto)", search)

    # attempt to extract anime_id
    anime_id = None
    try:
        j = search.get("json") or {}
        candidates = []
        # common shapes
        if isinstance(j, dict):
            d = j.get("data") or j.get("response") or j
            if isinstance(d, dict):
                # maybe contains response or list
                if "response" in d and isinstance(d["response"], list):
                    candidates = d["response"]
                else:
                    # if dict but has items that look like anime objects, try to find first
                    for v in d.values():
                        if isinstance(v, list):
                            candidates = v
                            break
            elif isinstance(d, list):
                candidates = d
        if candidates:
            first = candidates[0]
            if isinstance(first, dict):
                anime_id = first.get("id") or first.get("slug") or first.get("anime_id") or first.get("url")
    except Exception:
        anime_id = None

    write("Auto-extracted anime_id (if any): " + str(anime_id))

    # if no anime_id, user can run script with argument; otherwise proceed with placeholder
    if not anime_id:
        write("NOTE: could not auto-extract anime_id from search. Please run the script with a known anime_id if you have one.")
        write("Ending here (no anime_id).")
        return

    # 4. Anime details
    details = call(f"{BASE_URL}/anime/{anime_id}/", f"Anime details /anime/{anime_id}/")
    summarize_response(f"Anime details /anime/{anime_id}/", details)

    # 5. Episodes
    episodes = call(f"{BASE_URL}/episodes/{anime_id}/", f"Episodes /episodes/{anime_id}/")
    summarize_response(f"Episodes /episodes/{anime_id}/", episodes)

    # Save a small snippet for manual inspection (first 2000 chars)
    html_text = episodes.get("text") or ""
    if html_text:
        snippet = small_preview(html_text, 2000)
        with open(SNIPPET, "w", encoding="utf-8") as fh:
            fh.write(snippet)
        write(f"Saved HTML snippet to {SNIPPET} (first ~2000 chars).")

    # 5.a Check for syncData
    sync_snap = extract_syncdata_and_small_episodes(html_text or "")
    if sync_snap:
        write("Found syncData JSON snapshot:")
        write(json.dumps(sync_snap, indent=2, ensure_ascii=False))
    else:
        write("No usable #syncData JSON found in episodes HTML (or could not parse).")

    # 6. Try to detect episodes from response json if any
    eps_json = episodes.get("json")
    if eps_json and isinstance(eps_json, dict):
        # try common paths
        data = eps_json.get("data") or eps_json.get("response") or eps_json
        # try to shallow-print first 10 items if list
        if isinstance(data, list):
            write("Episodes list length (from JSON): " + str(len(data)))
            write("First up to 10 episode items (compact):")
            for i, it in enumerate(data[:10]):
                write(f" - [{i}] keys: {list(it.keys()) if isinstance(it, dict) else str(type(it))}")
        else:
            write("Episodes JSON returned but not a list; type: " + str(type(data)))
    else:
        write("Episodes JSON missing or not parseable.")

    # 7. Servers & Stream (best-effort): extract episode_id from episodes JSON
    episode_id = None
    try:
        if isinstance(eps_json, dict):
            d = eps_json.get("data") or eps_json.get("response") or eps_json
            if isinstance(d, list) and d:
                first = d[0]
                if isinstance(first, dict):
                    episode_id = first.get("id") or first.get("episode_id") or first.get("url")
    except Exception:
        episode_id = None

    write("Auto-extracted episode_id (if any): " + str(episode_id))

    if episode_id:
        srv = call(f"{BASE_URL}/servers/?id={episode_id}", f"Servers /servers/?id={episode_id}")
        summarize_response(f"Servers /servers/?id={episode_id}", srv)
        # small servers snapshot
        sj = srv.get("json")
        if isinstance(sj, dict):
            dd = sj.get("data") or sj
            write("Servers snapshot (sub/dub counts):")
            if isinstance(dd, dict):
                sub = dd.get("sub") or []
                dub = dd.get("dub") or []
                write(f"  sub_count: {len(sub) if isinstance(sub,list) else 'n/a'}")
                write(f"  dub_count: {len(dub) if isinstance(dub,list) else 'n/a'}")
                # show first 10 server items (compact)
                def compact_servers(arr, name):
                    if not isinstance(arr, list): return
                    write(f"  First up to 10 items from {name}:")
                    for i, s in enumerate(arr[:10]):
                        if isinstance(s, dict):
                            write(f"    - idx:{i} name:{s.get('name')} id:{s.get('id')} type:{s.get('type')}")
                        else:
                            write(f"    - {str(s)[:200]}")
                compact_servers(sub, "sub")
                compact_servers(dub, "dub")
        # try stream for first server (if exists)
        try:
            if isinstance(sj, dict) and sj.get("data"):
                dd = sj.get("data")
                servers_list = dd.get("sub") or dd.get("dub") or []
                if servers_list:
                    srvname = servers_list[0].get("name")
                    write("Attempting stream for server: " + str(srvname))
                    stream = call(f"{BASE_URL}/stream/?id={episode_id}&server={srvname}&type=sub", f"Stream /stream/?id={episode_id}&server={srvname}&type=sub")
                    summarize_response("Stream attempt", stream)
        except Exception as e:
            write("Stream attempt raised: " + str(e))
    else:
        write("No episode_id available; cannot test servers/stream automatically.")

    write("\nSummary complete. Please attach this file for debugging: " + OUTPUT)
    write("If you want, re-run with an explicit anime_id by setting BASE_URL env or editing script.")
    print("Done. Written compact summary to", OUTPUT, "and snippet to", SNIPPET)

if __name__ == "__main__":
    main()
