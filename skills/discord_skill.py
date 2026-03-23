import os
import requests
from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
_USE_MOCK = not DISCORD_WEBHOOK_URL or "xxxx" in DISCORD_WEBHOOK_URL


def send_discord_message(username: str, content: str) -> bool:
    """DiscordのWebhookを使ってメッセージを送信する。未設定時はコンソール出力。"""
    if _USE_MOCK:
        print(f"[Discord MOCK] {username}: {content}")
        return True

    payload = {
        "username": username,
        "content": content,
    }
    try:
        resp = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
        resp.raise_for_status()
        print(f"[Discord] {username}: {content}")
        return True
    except requests.RequestException as e:
        print(f"[Discord] 送信失敗: {e}")
        return False
