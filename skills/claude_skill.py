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
# MVMNTコンテキスト（プロンプト用・非公開情報）
# ============================================================

_MVMNT_CONTEXT = """
MVMNTは「暗号資産を日常で使えるようにする」ショッピングプラットフォームです。
核心テーマ:
- HODLからUSEへ：暗号資産を実際の買い物に使う体験
- 購入時に自動寄付＋ポイント還元（キャッシュバック）
- AIエージェントマーケットプレイス（自動販売・カスタマーサポート）
- コミュニティ予測市場（商品人気度の予測で利益化）
- 分散型信用スコア（買い物・寄付データから生成）
- VC資金を拒否、コミュニティ主導で運営
- 紹介プログラム（手数料100%還元モデル）

重要: MVMNTはまだ公開前のため、返信ドラフトではMVMNTに直接言及してはいけない。
代わりに、投稿のテーマに共感を示し、「こういうプラットフォームがあればいいのに」
「この方向性は正しいと思う」といった自然な形で会話に参加する方針。
"""

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
    """関数A: マーケティング分析。翻訳・危険度・熱量・返信ドラフトをJSONで返す。
    MVMNTには直接言及しない返信ドラフトを生成する。"""
    if USE_MOCK:
        print(f"[Claude MOCK] analyze_post: {title[:50]}")
        risk = random.randint(1, 10)
        heat = random.randint(1, 10)
        return {
            "title_ja": f"[翻訳] {title}",
            "body_ja": f"[翻訳] {body[:100]}..." if body else "(本文なし)",
            "risk_score": risk,
            "heat_score": heat,
            "reply_draft_en": "I've been thinking the same thing. The whole space needs platforms that let you actually spend crypto like normal money, with real cashback and community governance.",
            "reply_draft_ja": "同感です。暗号資産を普通のお金のように使えて、キャッシュバックやコミュニティ主導のガバナンスがあるプラットフォームが必要ですよね。",
        }

    client = _get_client()

    prompt = f"""あなたはWeb3マーケティングの専門家です。
以下のReddit投稿を分析し、**必ず下記のJSON形式のみ**で回答してください。

{_MVMNT_CONTEXT}

投稿タイトル: {title}
投稿本文: {body}

分析ルール:
- risk_score: 投稿への返信が炎上やネガティブ反応を招くリスク
- heat_score: 投稿自体の注目度・バズ度合い
- reply_draft_en/ja: MVMNTには一切言及せず、投稿のテーマに自然に共感する返信を作成。
  「自分もこういう体験がほしい」「この方向性は面白い」のような、同じ関心を持つ一般ユーザーの立場で書く。
  宣伝っぽさを完全に排除し、自然な会話として成立させること。

{{
  "title_ja": "タイトルの日本語訳",
  "body_ja": "本文の日本語訳（要約可）",
  "risk_score": 1-10の整数,
  "heat_score": 1-10の整数,
  "reply_draft_en": "英語での返信ドラフト（MVMNT言及禁止・自然な共感コメント）",
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
