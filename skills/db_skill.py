import os
from datetime import datetime, timezone

from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# ---------------------------------------------------------------------------
# Supabase client initialisation (with fallback to mock mode)
# ---------------------------------------------------------------------------
_client = None
_mock_mode = False

try:
    from supabase import create_client, Client

    if SUPABASE_URL and SUPABASE_KEY:
        _client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("[DB] Supabase クライアント初期化成功")
    else:
        _mock_mode = True
        print("[DB] SUPABASE_URL / SUPABASE_KEY が未設定のためモックモードで動作します")
except Exception as e:
    _mock_mode = True
    print(f"[DB] Supabase 接続に失敗しました。モックモードで動作します: {e}")

TABLE = "reddit_posts"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def save_analysis(post_data: dict, analysis: dict) -> bool:
    """分析結果を Supabase の reddit_posts テーブルに upsert する。"""

    row = {
        "id": post_data.get("id"),
        "title": post_data.get("title"),
        "selftext": post_data.get("selftext"),
        "url": post_data.get("url"),
        "subreddit": post_data.get("subreddit"),
        "score": post_data.get("score"),
        "num_comments": post_data.get("num_comments"),
        "created_utc": post_data.get("created_utc"),
        "title_ja": analysis.get("title_ja"),
        "body_ja": analysis.get("body_ja"),
        "risk_score": analysis.get("risk_score"),
        "heat_score": analysis.get("heat_score"),
        "reply_draft_en": analysis.get("reply_draft_en"),
        "reply_draft_ja": analysis.get("reply_draft_ja"),
        "analyzed_at": datetime.now(timezone.utc).isoformat(),
    }

    if _mock_mode or _client is None:
        print(f"[DB][MOCK] save_analysis: post_id={row['id']}")
        print(f"  risk={row['risk_score']}, heat={row['heat_score']}")
        return True

    try:
        _client.table(TABLE).upsert(row, on_conflict="id").execute()
        print(f"[DB] 保存完了: post_id={row['id']}")
        return True
    except Exception as e:
        print(f"[DB] 保存エラー: {e}")
        return False


def get_recent_posts(limit: int = 20) -> list[dict]:
    """最近の分析済み投稿を analyzed_at 降順で取得する。"""

    if _mock_mode or _client is None:
        print(f"[DB][MOCK] get_recent_posts: limit={limit}")
        return []

    try:
        response = (
            _client.table(TABLE)
            .select("*")
            .order("analyzed_at", desc=True)
            .limit(limit)
            .execute()
        )
        return response.data
    except Exception as e:
        print(f"[DB] 取得エラー: {e}")
        return []


# ---------------------------------------------------------------------------
# Farming History
# ---------------------------------------------------------------------------

FARMING_TABLE = "farming_history"


def save_farming_comment(post_id: str, subreddit: str, comment_id: str, comment_text: str) -> bool:
    """ファーミングコメントを farming_history テーブルに保存する。"""

    row = {
        "post_id": post_id,
        "subreddit": subreddit,
        "comment_id": comment_id,
        "comment_text": comment_text,
    }

    if _mock_mode or _client is None:
        print(f"[DB][MOCK] save_farming_comment: post_id={post_id}, subreddit={subreddit}, comment_id={comment_id}")
        return True

    try:
        _client.table(FARMING_TABLE).insert(row).execute()
        print(f"[DB] ファーミングコメント保存完了: comment_id={comment_id}")
        return True
    except Exception as e:
        print(f"[DB] ファーミングコメント保存エラー: {e}")
        return False


def get_farming_stats() -> dict:
    """ファーミング統計を取得する。合計コメント数とサブレディット別内訳を返す。"""

    if _mock_mode or _client is None:
        print("[DB][MOCK] get_farming_stats")
        return {"total": 0, "by_subreddit": {}}

    try:
        response = _client.table(FARMING_TABLE).select("subreddit").execute()
        rows = response.data
        total = len(rows)
        by_subreddit: dict[str, int] = {}
        for row in rows:
            sub = row.get("subreddit", "unknown")
            by_subreddit[sub] = by_subreddit.get(sub, 0) + 1
        return {"total": total, "by_subreddit": by_subreddit}
    except Exception as e:
        print(f"[DB] ファーミング統計取得エラー: {e}")
        return {"total": 0, "by_subreddit": {}}
