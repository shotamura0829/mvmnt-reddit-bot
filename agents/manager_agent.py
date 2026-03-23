from skills.db_skill import save_analysis
from skills.discord_skill import send_discord_message

AGENT_NAME = "📁 ManagerAgent"


def run(analysis_results: list[dict]) -> int:
    """分析結果をDBに保存し、Discordに報告する。"""
    if not analysis_results:
        send_discord_message(AGENT_NAME, "保存対象のデータがありません。")
        return 0

    send_discord_message(AGENT_NAME, f"📁 {len(analysis_results)}件のデータを保存中...")

    saved = 0
    for item in analysis_results:
        ok = save_analysis(item["post"], item["analysis"])
        if ok:
            saved += 1

    send_discord_message(
        AGENT_NAME,
        f"📁 DBに {saved}件 保存しダッシュボードへ連携しました！人間の指示を待ちます。",
    )
    return saved
