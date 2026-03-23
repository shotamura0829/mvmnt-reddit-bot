import os
import time
import random
from dotenv import load_dotenv

load_dotenv()

USE_MOCK = not os.getenv("REDDIT_CLIENT_ID") or os.getenv("REDDIT_CLIENT_ID") == "your_client_id"

_reddit = None

# ============================================================
# モックデータ
# ============================================================

_MOCK_RISING = [
    {
        "id": "mock_r1",
        "title": "What's a fact that sounds fake but is actually true?",
        "selftext": "",
        "url": "https://reddit.com/r/AskReddit/mock_r1",
        "subreddit": "AskReddit",
        "score": 42,
        "num_comments": 87,
        "created_utc": time.time() - 3600,
    },
    {
        "id": "mock_r2",
        "title": "People who wake up at 5am, what do you even do?",
        "selftext": "Seriously, the sun isn't even up yet.",
        "url": "https://reddit.com/r/AskReddit/mock_r2",
        "subreddit": "AskReddit",
        "score": 128,
        "num_comments": 215,
        "created_utc": time.time() - 1800,
    },
    {
        "id": "mock_r3",
        "title": "TIL honey never spoils. Archaeologists found 3000-year-old honey in Egyptian tombs that was still edible.",
        "selftext": "",
        "url": "https://reddit.com/r/todayilearned/mock_r3",
        "subreddit": "todayilearned",
        "score": 340,
        "num_comments": 56,
        "created_utc": time.time() - 7200,
    },
    {
        "id": "mock_r4",
        "title": "If you could add one rule to any sport, what would cause the most chaos?",
        "selftext": "",
        "url": "https://reddit.com/r/AskReddit/mock_r4",
        "subreddit": "AskReddit",
        "score": 95,
        "num_comments": 312,
        "created_utc": time.time() - 900,
    },
]

_MOCK_MVMNT_POSTS = [
    {
        "id": "mock_m1",
        "title": "Movement Labs just announced their mainnet launch date",
        "selftext": "Looks like Movement Network is going live next month. The Move VM approach is interesting compared to other L2s. Anyone else bullish?",
        "url": "https://reddit.com/r/CryptoCurrency/mock_m1",
        "subreddit": "CryptoCurrency",
        "score": 67,
        "num_comments": 23,
        "created_utc": time.time() - 5400,
    },
    {
        "id": "mock_m2",
        "title": "MVMNT token - worth looking into?",
        "selftext": "Heard about this new L2 project using Move VM. Their community seems active but I'm not sure about tokenomics. Thoughts?",
        "url": "https://reddit.com/r/altcoin/mock_m2",
        "subreddit": "altcoin",
        "score": 15,
        "num_comments": 8,
        "created_utc": time.time() - 10800,
    },
    {
        "id": "mock_m3",
        "title": "Comparing Move VM L2s: Movement vs Aptos vs Sui",
        "selftext": "I've been researching Move-based chains. Movement Network takes a different approach by building on Ethereum as an L2. Here's my comparison...",
        "url": "https://reddit.com/r/ethereum/mock_m3",
        "subreddit": "ethereum",
        "score": 203,
        "num_comments": 89,
        "created_utc": time.time() - 2700,
    },
]


# ============================================================
# 本番 Reddit クライアント
# ============================================================

def _get_reddit():
    global _reddit
    if _reddit is None:
        import praw
        _reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            username=os.getenv("REDDIT_USERNAME"),
            password=os.getenv("REDDIT_PASSWORD"),
            user_agent=os.getenv("REDDIT_USER_AGENT", "mvmnt-bot/0.1"),
        )
    return _reddit


# ============================================================
# 公開API
# ============================================================

def search_posts(keyword: str, subreddit: str = "all", limit: int = 10) -> list[dict]:
    """指定キーワードで投稿を検索し、リストで返す。"""
    if USE_MOCK:
        print(f"[Reddit MOCK] search_posts(keyword={keyword!r})")
        return [p for p in _MOCK_MVMNT_POSTS if keyword.lower() in p["title"].lower() or keyword.lower() in p["selftext"].lower()][:limit] or _MOCK_MVMNT_POSTS[:limit]

    reddit = _get_reddit()
    results = []
    for post in reddit.subreddit(subreddit).search(keyword, sort="new", limit=limit):
        results.append({
            "id": post.id,
            "title": post.title,
            "selftext": post.selftext[:500],
            "url": post.url,
            "subreddit": str(post.subreddit),
            "score": post.score,
            "num_comments": post.num_comments,
            "created_utc": post.created_utc,
        })
    return results


def get_rising_posts(subreddit: str = "AskReddit", limit: int = 10) -> list[dict]:
    """指定サブレディットのRising（急上昇）投稿を取得する。"""
    if USE_MOCK:
        print(f"[Reddit MOCK] get_rising_posts(subreddit={subreddit!r})")
        posts = [p for p in _MOCK_RISING if p["subreddit"] == subreddit] or _MOCK_RISING
        return random.sample(posts, min(limit, len(posts)))

    reddit = _get_reddit()
    results = []
    for post in reddit.subreddit(subreddit).rising(limit=limit):
        results.append({
            "id": post.id,
            "title": post.title,
            "selftext": post.selftext[:500],
            "url": post.url,
            "subreddit": str(post.subreddit),
            "score": post.score,
            "num_comments": post.num_comments,
            "created_utc": post.created_utc,
        })
    return results


def post_comment(post_id: str, body: str) -> str | None:
    """指定投稿にコメントを書き込み、コメントIDを返す。"""
    if USE_MOCK:
        fake_id = f"mock_comment_{random.randint(1000, 9999)}"
        print(f"[Reddit MOCK] コメント投稿: {fake_id} on {post_id}")
        print(f"  内容: {body[:80]}...")
        return fake_id

    reddit = _get_reddit()
    try:
        submission = reddit.submission(id=post_id)
        comment = submission.reply(body)
        print(f"[Reddit] コメント投稿完了: {comment.id} on {post_id}")
        return comment.id
    except Exception as e:
        print(f"[Reddit] コメント投稿失敗: {e}")
        return None
