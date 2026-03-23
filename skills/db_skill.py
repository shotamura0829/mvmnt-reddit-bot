import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def save_analysis(post_data: dict, analysis: dict) -> bool:
    """分析結果をSupabaseに保存する（ダミー実装）。"""
    print(f"[DB] 保存処理（ダミー）: post_id={post_data.get('id')}")
    print(f"  risk={analysis.get('risk_score')}, heat={analysis.get('heat_score')}")
    print(f"  URL: {SUPABASE_URL}")
    return True


def get_recent_posts(limit: int = 20) -> list[dict]:
    """最近の投稿を取得する（ダミー実装）。"""
    print(f"[DB] 最近の投稿を取得（ダミー）: limit={limit}")
    return []
