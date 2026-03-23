import time
import random
from skills.reddit_skill import get_rising_posts, post_comment, USE_MOCK
from skills.claude_skill import generate_warmup_comment
from skills.discord_skill import send_discord_message

AGENT_NAME = "👩‍🌾 FarmerAgent"
WARMUP_SUBREDDITS = ["AskReddit", "Showerthoughts", "mildlyinteresting", "todayilearned"]


def run(max_comments: int = 3, delay_range: tuple = (30, 90)):
    """一般サブレディットを巡回し、自然なコメントを投稿してカルマを稼ぐ。"""
    send_discord_message(AGENT_NAME, "🌾 ウォームアップ巡回を開始します...")

    subreddit = random.choice(WARMUP_SUBREDDITS)
    send_discord_message(AGENT_NAME, f"r/{subreddit} のRising投稿をチェック中...")

    posts = get_rising_posts(subreddit=subreddit, limit=max_comments + 5)
    if not posts:
        send_discord_message(AGENT_NAME, f"r/{subreddit} で投稿が見つかりませんでした。")
        return []

    commented = []
    for post in posts[:max_comments]:
        comment_text = generate_warmup_comment(post["title"], post["selftext"])
        send_discord_message(
            AGENT_NAME,
            f"💬 コメント案: \"{comment_text[:80]}...\" → `{post['title'][:50]}`",
        )

        comment_id = post_comment(post["id"], comment_text)
        if comment_id:
            commented.append({
                "post_id": post["id"],
                "subreddit": post["subreddit"],
                "comment_id": comment_id,
                "comment_text": comment_text,
            })

        if USE_MOCK:
            delay = 1
        else:
            delay = random.randint(*delay_range)
        send_discord_message(AGENT_NAME, f"⏳ 次のコメントまで {delay}秒 待機...")
        time.sleep(delay)

    send_discord_message(
        AGENT_NAME,
        f"👩‍🌾 ウォームアップ完了！ r/{subreddit} で雑談してカルマを稼いできました🌱 "
        f"({len(commented)}件コメント)",
    )
    return commented
