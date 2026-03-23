"""
MVMNT Reddit マーケティング自動化 - マルチエージェントオーケストレーター

Usage:
    python main.py warmup          # ウォームアップモード（Farmerのみ）
    python main.py marketing       # マーケティングモード（Scout→Analyst→Manager）
    python main.py all             # 両方実行
"""

import sys
from skills.discord_skill import send_discord_message
from agents import farmer_agent, scout_agent, analyst_agent, manager_agent


def run_warmup():
    """ウォームアップモード: Farmerがカルマを稼ぐ。"""
    send_discord_message("🤖 Orchestrator", "=== ウォームアップモード開始 ===")
    farmer_agent.run(max_comments=3)
    send_discord_message("🤖 Orchestrator", "=== ウォームアップモード完了 ===")


def run_marketing():
    """マーケティングモード: Scout → Analyst → Manager の連携。"""
    send_discord_message("🤖 Orchestrator", "=== マーケティングモード開始 ===")

    # Step 1: Scout が投稿を探索
    posts = scout_agent.run()

    if not posts:
        send_discord_message("🤖 Orchestrator", "関連投稿なし。終了します。")
        return

    # Step 2: Analyst が分析
    results = analyst_agent.run(posts)

    # Step 3: Manager がDB保存
    manager_agent.run(results)

    send_discord_message("🤖 Orchestrator", "=== マーケティングモード完了 ===")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "marketing"

    if mode == "warmup":
        run_warmup()
    elif mode == "marketing":
        run_marketing()
    elif mode == "all":
        run_warmup()
        run_marketing()
    else:
        print(f"Unknown mode: {mode}")
        print("Usage: python main.py [warmup|marketing|all]")
        sys.exit(1)


if __name__ == "__main__":
    main()
