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
        "title": "Is there any platform where I can actually spend crypto like normal money?",
        "selftext": "I have a decent bag but there's literally nowhere to spend it on everyday stuff. Everything is just speculation. I want to buy things, get cashback, feel like crypto is actually useful.",
        "url": "https://reddit.com/r/CryptoCurrency/mock_m1",
        "subreddit": "CryptoCurrency",
        "score": 312,
        "num_comments": 145,
        "created_utc": time.time() - 3600,
    },
    {
        "id": "mock_m2",
        "title": "Tired of HODL culture. When do we actually USE crypto?",
        "selftext": "Everyone says HODL but what's the point if you never spend it? I'd love a platform that lets me shop with crypto and get rewards, like a crypto version of Rakuten.",
        "url": "https://reddit.com/r/CryptoCurrency/mock_m2",
        "subreddit": "CryptoCurrency",
        "score": 89,
        "num_comments": 67,
        "created_utc": time.time() - 7200,
    },
    {
        "id": "mock_m3",
        "title": "AI agents for e-commerce - anyone building this?",
        "selftext": "I'm curious about AI agents that can handle shopping, customer support, and even negotiate prices autonomously. Seems like a huge opportunity.",
        "url": "https://reddit.com/r/artificial/mock_m3",
        "subreddit": "artificial",
        "score": 156,
        "num_comments": 43,
        "created_utc": time.time() - 5400,
    },
    {
        "id": "mock_m4",
        "title": "Why are all crypto projects funded by VCs? Where's the community-owned stuff?",
        "selftext": "Every new project is backed by a16z or some VC. The tokens are pre-allocated, insiders dump on retail. Where are the truly community-funded projects?",
        "url": "https://reddit.com/r/defi/mock_m4",
        "subreddit": "defi",
        "score": 234,
        "num_comments": 98,
        "created_utc": time.time() - 1800,
    },
    {
        "id": "mock_m5",
        "title": "Prediction markets for consumer products - would you use this?",
        "selftext": "Imagine betting on which products will be popular next quarter, or whether a brand's delivery will improve. Like Polymarket but for shopping.",
        "url": "https://reddit.com/r/web3/mock_m5",
        "subreddit": "web3",
        "score": 45,
        "num_comments": 22,
        "created_utc": time.time() - 10800,
    },
    {
        "id": "mock_m6",
        "title": "Crypto cashback rewards - which platforms actually work?",
        "selftext": "Looking for platforms that give crypto cashback on purchases. Not credit cards, actual crypto-native shopping platforms with real rewards.",
        "url": "https://reddit.com/r/ethfinance/mock_m6",
        "subreddit": "ethfinance",
        "score": 78,
        "num_comments": 31,
        "created_utc": time.time() - 900,
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
