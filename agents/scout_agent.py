from skills.reddit_skill import search_posts
from skills.discord_skill import send_discord_message

AGENT_NAME = "🔍 ScoutAgent"

# ============================================================
# キーワード戦略（MVMNTには直接言及しない）
#
# MVMNTの核心テーマ:
#   - 暗号資産を「使う」ショッピング体験
#   - コミュニティ主導・VC排除
#   - AIエージェントによるコマース
#   - 予測市場
#   - 分散型信用スコア
#
# → これらのテーマに関心がある層が集まるスレッドを探す
# ============================================================

DEFAULT_KEYWORDS = [
    # 暗号資産×実用・決済
    "spend crypto shopping",
    "pay with crypto",
    "crypto payments real world",
    "use cryptocurrency buy",
    # HODL文化への疑問
    "tired of holding crypto",
    "crypto actually useful",
    "when will crypto be usable",
    # コミュニティ・DAO・VC批判
    "community funded crypto",
    "no VC crypto project",
    "community owned platform",
    # AI × コマース
    "AI agent marketplace",
    "AI shopping assistant",
    "autonomous AI agents commerce",
    # 予測市場
    "prediction market crypto",
    "consumer prediction market",
    # Web3ショッピング
    "web3 shopping",
    "onchain commerce",
    "crypto cashback rewards",
]

# テーマカテゴリ（Discord報告用）
KEYWORD_CATEGORIES = {
    "crypto_spending": ["spend crypto shopping", "pay with crypto", "crypto payments real world", "use cryptocurrency buy"],
    "hodl_fatigue": ["tired of holding crypto", "crypto actually useful", "when will crypto be usable"],
    "community_first": ["community funded crypto", "no VC crypto project", "community owned platform"],
    "ai_commerce": ["AI agent marketplace", "AI shopping assistant", "autonomous AI agents commerce"],
    "prediction_market": ["prediction market crypto", "consumer prediction market"],
    "web3_shopping": ["web3 shopping", "onchain commerce", "crypto cashback rewards"],
}


def _get_category(keyword: str) -> str:
    for cat, kws in KEYWORD_CATEGORIES.items():
        if keyword in kws:
            return cat
    return "other"


def run(keywords: list[str] | None = None, limit: int = 5) -> list[dict]:
    """MVMNTのテーマに関連する投稿を探索し、Discordに報告する。"""
    keywords = keywords or DEFAULT_KEYWORDS
    send_discord_message(AGENT_NAME, f"🔍 {len(keywords)}個のキーワードで探索開始...")

    all_posts = []
    seen_ids = set()
    category_hits = {}

    for kw in keywords:
        posts = search_posts(keyword=kw, limit=limit)
        cat = _get_category(kw)
        for p in posts:
            if p["id"] not in seen_ids:
                seen_ids.add(p["id"])
                p["matched_keyword"] = kw
                p["category"] = cat
                all_posts.append(p)
                category_hits[cat] = category_hits.get(cat, 0) + 1

    if not all_posts:
        send_discord_message(AGENT_NAME, "関連投稿は見つかりませんでした。")
        return []

    # カテゴリ別サマリーを報告
    cat_labels = {
        "crypto_spending": "💳 暗号資産決済",
        "hodl_fatigue": "😤 HODL疲れ",
        "community_first": "🤝 コミュニティ主導",
        "ai_commerce": "🤖 AI×コマース",
        "prediction_market": "📈 予測市場",
        "web3_shopping": "🛒 Web3ショッピング",
    }
    summary = " / ".join(
        f"{cat_labels.get(c, c)}: {n}件" for c, n in category_hits.items()
    )
    send_discord_message(AGENT_NAME, f"📊 カテゴリ別: {summary}")

    for post in all_posts[:10]:  # 上位10件を報告
        send_discord_message(
            AGENT_NAME,
            f"📌 [{post['subreddit']}] {post['title'][:60]} "
            f"(🔑 {post['matched_keyword'][:30]})",
        )

    send_discord_message(
        AGENT_NAME,
        f"🔍 関連投稿を {len(all_posts)}件 発見！ Analystさん分析をお願いします！",
    )
    return all_posts
