from skills.reddit_skill import search_posts
from skills.discord_skill import send_discord_message

AGENT_NAME = "🔍 ScoutAgent"
DEFAULT_KEYWORDS = ["MVMNT", "Movement Labs", "Movement Network", "Move VM"]


def run(keywords: list[str] | None = None, limit: int = 10) -> list[dict]:
    """MVMNT関連の投稿を探索し、Discordに報告する。"""
    keywords = keywords or DEFAULT_KEYWORDS
    send_discord_message(AGENT_NAME, f"🔍 キーワード {keywords} で探索開始...")

    all_posts = []
    seen_ids = set()

    for kw in keywords:
        posts = search_posts(keyword=kw, limit=limit)
        for p in posts:
            if p["id"] not in seen_ids:
                seen_ids.add(p["id"])
                all_posts.append(p)

    if not all_posts:
        send_discord_message(AGENT_NAME, "関連投稿は見つかりませんでした。")
        return []

    for post in all_posts:
        send_discord_message(
            AGENT_NAME,
            f"📌 [{post['subreddit']}] {post['title'][:60]} (score: {post['score']})",
        )

    send_discord_message(
        AGENT_NAME,
        f"🔍 新しい関連投稿を {len(all_posts)}件 発見！ Analystさん分析をお願いします！",
    )
    return all_posts
