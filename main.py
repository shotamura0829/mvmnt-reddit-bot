"""
MVMNT Reddit マーケティング自動化 - マルチエージェントオーケストレーター

Usage:
    python main.py warmup          # ウォームアップモード（Farmerのみ）
    python main.py marketing       # マーケティングモード（Scout→Analyst→Manager）
    python main.py all             # 両方実行
    python main.py scheduler       # スケジューラモード（warmup: 2h, marketing: 30m）
"""

import sys
import time
from datetime import datetime, timedelta
from skills.discord_skill import send_discord_message
from agents import farmer_agent, scout_agent, analyst_agent, manager_agent

WARMUP_INTERVAL = 2 * 60 * 60   # 2 hours in seconds
MARKETING_INTERVAL = 30 * 60     # 30 minutes in seconds


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


def run_scheduler():
    """スケジューラモード: warmup を2時間毎、marketing を30分毎に繰り返す。"""
    print(f"[Scheduler] スケジューラモード開始: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[Scheduler] Warmup 間隔: {WARMUP_INTERVAL // 3600}時間")
    print(f"[Scheduler] Marketing 間隔: {MARKETING_INTERVAL // 60}分")
    print("[Scheduler] 停止するには Ctrl+C を押してください")
    send_discord_message("🤖 Orchestrator", "=== スケジューラモード開始 ===")

    now = time.time()
    next_warmup = now
    next_marketing = now

    try:
        while True:
            now = time.time()

            if now >= next_warmup:
                ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"\n[Scheduler][{ts}] Warmup 実行中...")
                try:
                    run_warmup()
                except Exception as e:
                    print(f"[Scheduler] Warmup エラー: {e}")
                next_warmup = time.time() + WARMUP_INTERVAL
                next_warmup_str = (datetime.now() + timedelta(seconds=WARMUP_INTERVAL)).strftime('%Y-%m-%d %H:%M:%S')
                print(f"[Scheduler] 次の Warmup: {next_warmup_str}")

            if now >= next_marketing:
                ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"\n[Scheduler][{ts}] Marketing 実行中...")
                try:
                    run_marketing()
                except Exception as e:
                    print(f"[Scheduler] Marketing エラー: {e}")
                next_marketing = time.time() + MARKETING_INTERVAL
                next_marketing_str = (datetime.now() + timedelta(seconds=MARKETING_INTERVAL)).strftime('%Y-%m-%d %H:%M:%S')
                print(f"[Scheduler] 次の Marketing: {next_marketing_str}")

            # Sleep until the next task is due (check every 10 seconds at most)
            next_run = min(next_warmup, next_marketing)
            sleep_time = max(1, next_run - time.time())
            time.sleep(min(sleep_time, 10))

    except KeyboardInterrupt:
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n[Scheduler][{ts}] Ctrl+C を検出しました。スケジューラを停止します。")
        send_discord_message("🤖 Orchestrator", "=== スケジューラモード停止 ===")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "marketing"

    if mode == "warmup":
        run_warmup()
    elif mode == "marketing":
        run_marketing()
    elif mode == "all":
        run_warmup()
        run_marketing()
    elif mode == "scheduler":
        run_scheduler()
    else:
        print(f"Unknown mode: {mode}")
        print("Usage: python main.py [warmup|marketing|all|scheduler]")
        sys.exit(1)


if __name__ == "__main__":
    main()
