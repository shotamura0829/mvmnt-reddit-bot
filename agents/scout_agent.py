import time
import random
from skills.reddit_skill import search_posts
from skills.discord_skill import send_discord_message

AGENT_NAME = "🔍 ScoutAgent"

# ============================================================
# キーワード戦略（厳選6個 - 各カテゴリ代表1つ）
# ============================================================

# (キーワード, 検索対象サブレディット)
DEFAULT_KEYWORDS = [
    ("pay with crypto", "CryptoCurrency+ethereum+defi+web3+ethfinance"),
    ("tired of holding crypto", "CryptoCurrency+ethereum+defi+Bitcoin"),
    ("community owned crypto", "CryptoCurrency+defi+web3+ethfinance"),
    ("AI agent marketplace", "CryptoCurrency+artificial+web3+MachineLearning"),
    ("prediction market crypto", "CryptoCurrency+defi+web3+ethereum"),
    ("crypto cashback rewards", "CryptoCurrency+defi+web3+ethfinance"),
]

KEYWORD_CATEGORIES = {
    "pay with crypto": ("crypto_spending", "💳 暗号資産決済"),
    "tired of holding crypto": ("hodl_fatigue", "😤 HODL疲れ"),
    "community owned crypto": ("community_first", "🤝 コミュニティ主導"),
    "AI agent marketplace": ("ai_commerce", "🤖 AI×コマース"),
    "prediction market crypto": ("prediction_market", "📈 予測市場"),
    "crypto cashback rewards": ("web3_shopping", "🛒 Web3ショッピング"),
}

# 分析対象の最大件数（Claude API呼び出し数を制限）
MAX_ANALYZE = 10


def run(keywords: list | None = None, limit: int = 5) -> list[dict]:
    """MVMNTのテーマに関連する投稿を探索し、Discordに報告する。"""
    keywords = keywords or DEFAULT_KEYWORDS
    send_discord_message(AGENT_NAME, f"🔍 {len(keywords)}個のキーワードで探索開始...")

    all_posts = []
    seen_ids = set()
    category_hits = {}

    for entry in keywords:
        if isinstance(entry, tuple):
            kw, subreddit = entry
        else:
            kw, subreddit = entry, "all"
        posts = search_posts(keyword=kw, subreddit=subreddit, limit=limit)
        cat_id, cat_label = KEYWORD_CATEGORIES.get(kw, ("other", "Other"))
        for p in posts:
            # score > 0 のみ（ノイズ除去）
            if p["id"] not in seen_ids and p["score"] > 0:
                seen_ids.add(p["id"])
                p["matched_keyword"] = kw
                p["category"] = cat_id
                all_posts.append(p)
                category_hits[cat_label] = category_hits.get(cat_label, 0) + 1

        # Reddit APIレート制限対策（1秒待機）
        time.sleep(1)

    if not all_posts:
        send_discord_message(AGENT_NAME, "関連投稿は見つかりませんでした。")
        return []

    # スコア順にソート
    all_posts.sort(key=lambda p: p["score"], reverse=True)

    # カテゴリ別サマリーを報告
    summary = " / ".join(f"{c}: {n}件" for c, n in category_hits.items())
    send_discord_message(AGENT_NAME, f"📊 カテゴリ別: {summary}")

    # 上位のみ報告・分析対象に
    top_posts = all_posts[:MAX_ANALYZE]
    for post in top_posts:
        send_discord_message(
            AGENT_NAME,
            f"📌 [{post['subreddit']}] {post['title'][:60]} (score: {post['score']})",
        )

    send_discord_message(
        AGENT_NAME,
        f"🔍 {len(all_posts)}件中 上位{len(top_posts)}件を分析対象に！ Analystさんお願いします！",
    )
    return top_posts
