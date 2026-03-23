"use client";

import { useState } from "react";
import type { RedditPost } from "@/lib/supabase";
import RiskBadge from "./RiskBadge";

function timeAgo(dateStr: string) {
  const diff = Date.now() - new Date(dateStr).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 60) return `${mins}m ago`;
  const hours = Math.floor(mins / 60);
  if (hours < 24) return `${hours}h ago`;
  return `${Math.floor(hours / 24)}d ago`;
}

export default function PostCard({ post }: { post: RedditPost }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div
      className="glass-card rounded-2xl p-6 hover:bg-card-hover transition-all duration-300 cursor-pointer group"
      onClick={() => setExpanded(!expanded)}
    >
      {/* Header */}
      <div className="flex items-start justify-between gap-4 mb-3">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-xs font-medium text-accent-light bg-accent/10 px-2.5 py-1 rounded-full">
              r/{post.subreddit}
            </span>
            <span className="text-xs text-muted">
              {timeAgo(post.analyzed_at)}
            </span>
          </div>
          {/* English title (main) */}
          <h3 className="font-semibold text-foreground group-hover:text-accent-light transition-colors leading-snug">
            {post.title}
          </h3>
          {/* Japanese translation (sub) */}
          {post.title_ja && (
            <p className="text-sm text-muted mt-1">
              {post.title_ja}
            </p>
          )}
        </div>
      </div>

      {/* Scores */}
      <div className="flex items-center gap-2 mb-3">
        <RiskBadge score={post.risk_score} label="Risk" />
        <RiskBadge score={post.heat_score} label="Heat" />
        <span className="text-xs text-muted ml-auto">
          {post.score} pts &middot; {post.num_comments} comments
        </span>
      </div>

      {/* Body (expandable) */}
      {expanded && (
        <div className="mt-4 space-y-4 animate-in fade-in duration-200">
          {/* Post body - English */}
          <div>
            <p className="text-xs font-semibold text-muted uppercase tracking-wider mb-2">
              Original Post
            </p>
            <div className="bg-background rounded-xl p-4 border border-border">
              <p className="text-sm leading-relaxed">
                {post.selftext || "(No body)"}
              </p>
            </div>
            {/* Japanese translation */}
            {post.body_ja && (
              <div className="bg-background/50 rounded-xl p-4 border border-border/50 mt-2">
                <p className="text-xs text-accent-light mb-1 font-medium">🇯🇵 日本語訳</p>
                <p className="text-sm text-muted leading-relaxed">
                  {post.body_ja}
                </p>
              </div>
            )}
          </div>

          {/* Reply Draft - English (main, this is what gets posted) */}
          <div>
            <p className="text-xs font-semibold text-muted uppercase tracking-wider mb-2">
              Reply Draft (English)
            </p>
            <div className="bg-accent/5 border border-accent/20 rounded-xl p-4">
              <p className="text-sm leading-relaxed">
                {post.reply_draft_en || "-"}
              </p>
            </div>
            {/* Japanese reference translation */}
            {post.reply_draft_ja && (
              <div className="bg-background/50 rounded-xl p-4 border border-border/50 mt-2">
                <p className="text-xs text-accent-light mb-1 font-medium">🇯🇵 参考訳</p>
                <p className="text-sm text-muted leading-relaxed">
                  {post.reply_draft_ja}
                </p>
              </div>
            )}
          </div>

          {/* Link */}
          <div className="flex justify-end">
            <a
              href={post.url}
              target="_blank"
              rel="noopener noreferrer"
              onClick={(e) => e.stopPropagation()}
              className="text-xs text-accent-light hover:underline"
            >
              Open on Reddit &rarr;
            </a>
          </div>
        </div>
      )}
    </div>
  );
}
