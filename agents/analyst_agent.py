from skills.claude_skill import analyze_post
from skills.discord_skill import send_discord_message

AGENT_NAME = "🧠 AnalystAgent"


def run(posts: list[dict]) -> list[dict]:
    """投稿リストを分析し、結果をDiscordに報告する。"""
    if not posts:
        send_discord_message(AGENT_NAME, "分析対象の投稿がありません。")
        return []

    send_discord_message(AGENT_NAME, f"🧠 {len(posts)}件の投稿を分析開始...")

    results = []
    for post in posts:
        analysis = analyze_post(post["title"], post["selftext"])

        risk = analysis.get("risk_score", "?")
        heat = analysis.get("heat_score", "?")
        title_ja = analysis.get("title_ja", post["title"])

        send_discord_message(
            AGENT_NAME,
            f"📊 「{title_ja[:40]}」 → 危険度: {risk}/10, 熱量: {heat}/10",
        )

        results.append({"post": post, "analysis": analysis})

    send_discord_message(
        AGENT_NAME,
        f"🧠 分析完了。{len(results)}件処理しました。Managerさん記録をお願いします！",
    )
    return results
