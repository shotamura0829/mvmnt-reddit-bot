import os
import json
import random
from dotenv import load_dotenv

load_dotenv()

USE_MOCK = not os.getenv("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_API_KEY") == "your_anthropic_api_key"

_client = None


def _get_client():
    global _client
    if _client is None:
        import anthropic
        _client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    return _client


# ============================================================
# モックデータ
# ============================================================

_MOCK_WARMUP_COMMENTS = [
    "Honey is basically the cockroach of foods — it simply refuses to die.",
    "I tried waking up at 5am once. My body filed a formal complaint.",
    "Adding a mandatory dance-off after every foul would fix every sport instantly.",
    "As someone who peaked in middle school, I feel personally attacked by this post.",
    "The real question is who hurt you enough to make you post this at 3am.",
]


def analyze_post(title: str, body: str) -> dict:
    """関数A: マーケティング分析。翻訳・危険度・熱量・返信ドラフトをJSONで返す。"""
    if USE_MOCK:
        print(f"[Claude MOCK] analyze_post: {title[:50]}")
        risk = random.randint(1, 10)
        heat = random.randint(1, 10)
        return {
            "title_ja": f"[翻訳] {title}",
            "body_ja": f"[翻訳] {body[:100]}..." if body else "(本文なし)",
            "risk_score": risk,
            "heat_score": heat,
            "reply_draft_en": f"Great post! Movement Network's approach with Move VM on Ethereum L2 is worth watching.",
            "reply_draft_ja": f"素晴らしい投稿です！Movement NetworkのMove VM on Ethereum L2のアプローチは注目に値します。",
        }

    client = _get_client()

    prompt = f"""あなたはWeb3マーケティングの専門家です。
以下のReddit投稿を分析し、**必ず下記のJSON形式のみ**で回答してください。

投稿タイトル: {title}
投稿本文: {body}

{{
  "title_ja": "タイトルの日本語訳",
  "body_ja": "本文の日本語訳（要約可）",
  "risk_score": 1-10の整数（1=安全, 10=炎上リスク大）,
  "heat_score": 1-10の整数（1=無関心, 10=バズ中）,
  "reply_draft_en": "英語での返信ドラフト",
  "reply_draft_ja": "日本語での返信ドラフト"
}}"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    text = message.content[0].text
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}") + 1
        if start != -1 and end > start:
            return json.loads(text[start:end])
        return {"raw": text, "error": "JSON parse failed"}


def generate_warmup_comment(title: str, body: str) -> str:
    """関数B: ウォームアップ用。MVMNTに一切触れず、短くユーモアのある自然なコメントを生成。"""
    if USE_MOCK:
        print(f"[Claude MOCK] generate_warmup_comment: {title[:50]}")
        return random.choice(_MOCK_WARMUP_COMMENTS)

    client = _get_client()

    prompt = f"""You are a casual Reddit user. Write a short, witty, and natural-sounding comment
for the following post. Rules:
- Keep it under 2 sentences.
- Sound like a real human, use humor if appropriate.
- Do NOT mention any crypto, Web3, blockchain, or any project names.
- Just be a friendly Redditor.

Post title: {title}
Post body: {body}

Reply with ONLY the comment text, nothing else."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text.strip()
