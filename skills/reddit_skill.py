"""
Reddit データ取得スキル

認証不要の公開JSON APIを使用してRedditの投稿を取得する。
コメント投稿（書き込み）はAPI認証が必要なため、ダッシュボードから手動で行う。
"""

import time
import random
import requests

_HEADERS = {
    "User-Agent": "mvmnt-bot/0.1 (reddit marketing intelligence)",
}
_BASE = "https://www.reddit.com"


def _parse_posts(data: dict) -> list[dict]:
    """RedditのJSON応答から投稿リストをパースする。"""
    results = []
    children = data.get("data", {}).get("children", [])
    for child in children:
        p = child.get("data", {})
        if not p.get("id"):
            continue
        results.append({
            "id": p["id"],
            "title": p.get("title", ""),
            "selftext": (p.get("selftext") or "")[:500],
            "url": f"https://reddit.com{p.get('permalink', '')}",
            "subreddit": p.get("subreddit", ""),
            "score": p.get("score", 0),
            "num_comments": p.get("num_comments", 0),
            "created_utc": p.get("created_utc", 0),
        })
    return results


def _fetch_json(url: str, params: dict | None = None) -> dict | None:
    """Reddit公開JSON APIからデータを取得する。"""
    try:
        resp = requests.get(url, headers=_HEADERS, params=params, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"[Reddit] API取得失敗: {e}")
        return None


def search_posts(keyword: str, subreddit: str = "all", limit: int = 10) -> list[dict]:
    """指定キーワードで投稿を検索し、リストで返す。"""
    print(f"[Reddit] search_posts(keyword={keyword!r}, subreddit={subreddit!r})")
    url = f"{_BASE}/r/{subreddit}/search.json"
    params = {"q": keyword, "sort": "new", "limit": limit, "restrict_sr": 1 if subreddit != "all" else 0}
    data = _fetch_json(url, params)
    if not data:
        return []
    return _parse_posts(data)


def get_rising_posts(subreddit: str = "AskReddit", limit: int = 10) -> list[dict]:
    """指定サブレディットのRising（急上昇）投稿を取得する。"""
    print(f"[Reddit] get_rising_posts(subreddit={subreddit!r})")
    url = f"{_BASE}/r/{subreddit}/rising.json"
    params = {"limit": limit}
    data = _fetch_json(url, params)
    if not data:
        # risingが空の場合、hotにフォールバック
        print(f"[Reddit] Rising が空のため Hot にフォールバック")
        url = f"{_BASE}/r/{subreddit}/hot.json"
        data = _fetch_json(url, params)
    if not data:
        return []
    return _parse_posts(data)


def post_comment(post_id: str, body: str) -> str | None:
    """コメント投稿（API認証が必要なため、現在はログのみ）。
    実際の投稿はダッシュボードからCopy Reply → 手動で行う。"""
    print(f"[Reddit] ⚠️ コメント投稿はAPI認証が必要です（手動投稿してください）")
    print(f"  投稿先: https://reddit.com/comments/{post_id}")
    print(f"  内容: {body[:100]}...")
    # ダミーIDを返してフローを継続させる
    return f"manual_{post_id}_{random.randint(1000, 9999)}"
