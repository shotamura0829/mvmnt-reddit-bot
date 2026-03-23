"use client";

import { useEffect, useState, useCallback } from "react";
import { supabase } from "@/lib/supabase";
import type { RedditPost } from "@/lib/supabase";
import type { User } from "@supabase/supabase-js";
import Header from "./Header";
import StatsCard from "./StatsCard";
import PostCard from "./PostCard";

type ScoreFilter = "all" | "high_risk" | "hot";
type StatusFilter = "all" | "pending" | "approved" | "posted" | "skipped";

export default function Dashboard() {
  const [user, setUser] = useState<User | null>(null);
  const [posts, setPosts] = useState<RedditPost[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<ScoreFilter>("all");
  const [statusFilter, setStatusFilter] = useState<StatusFilter>("all");

  const fetchPosts = useCallback(async () => {
    const { data } = await supabase
      .from("reddit_posts")
      .select("*")
      .order("analyzed_at", { ascending: false })
      .limit(50);
    if (data) setPosts(data);
    setLoading(false);
  }, []);

  useEffect(() => {
    supabase.auth.getUser().then(({ data }) => setUser(data.user));
    fetchPosts();

    // Real-time subscription
    const channel = supabase
      .channel("reddit_posts_changes")
      .on(
        "postgres_changes",
        { event: "*", schema: "public", table: "reddit_posts" },
        () => fetchPosts()
      )
      .subscribe();

    return () => {
      supabase.removeChannel(channel);
    };
  }, [fetchPosts]);

  const filteredPosts = posts.filter((p) => {
    // Score filter
    if (filter === "high_risk" && p.risk_score < 7) return false;
    if (filter === "hot" && p.heat_score < 7) return false;
    // Status filter
    if (statusFilter !== "all") {
      const postStatus = p.status || "pending";
      if (postStatus !== statusFilter) return false;
    }
    return true;
  });

  const avgRisk =
    posts.length > 0
      ? (posts.reduce((s, p) => s + (p.risk_score || 0), 0) / posts.length).toFixed(1)
      : "0";
  const avgHeat =
    posts.length > 0
      ? (posts.reduce((s, p) => s + (p.heat_score || 0), 0) / posts.length).toFixed(1)
      : "0";
  const subreddits = new Set(posts.map((p) => p.subreddit)).size;
  const pendingCount = posts.filter((p) => !p.status || p.status === "pending").length;

  const statusTabs: { key: StatusFilter; label: string }[] = [
    { key: "all", label: "All" },
    { key: "pending", label: "Pending" },
    { key: "approved", label: "Approved" },
    { key: "posted", label: "Posted" },
    { key: "skipped", label: "Skipped" },
  ];

  function statusCount(s: StatusFilter): number {
    if (s === "all") return posts.length;
    return posts.filter((p) => (p.status || "pending") === s).length;
  }

  return (
    <div className="min-h-screen">
      {/* Background decoration */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 left-1/3 w-[600px] h-[600px] bg-accent/3 rounded-full blur-3xl" />
        <div className="absolute bottom-0 right-1/4 w-[500px] h-[500px] bg-purple-500/3 rounded-full blur-3xl" />
      </div>

      <Header user={user} />

      <main className="relative max-w-7xl mx-auto px-6 py-8">
        {/* Stats */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <StatsCard
            label="Total Posts"
            value={posts.length}
            sub="analyzed"
            icon={
              <svg width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            }
            color="accent"
          />
          <StatsCard
            label="Pending"
            value={pendingCount}
            sub="awaiting review"
            icon={
              <svg width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            }
            color={pendingCount > 0 ? "warning" : "success"}
          />
          <StatsCard
            label="Avg Risk"
            value={avgRisk}
            sub="/ 10"
            icon={
              <svg width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4.5c-.77-.833-2.694-.833-3.464 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            }
            color={Number(avgRisk) > 6 ? "danger" : Number(avgRisk) > 3 ? "warning" : "success"}
          />
          <StatsCard
            label="Avg Heat"
            value={avgHeat}
            sub="/ 10"
            icon={
              <svg width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z" />
              </svg>
            }
            color={Number(avgHeat) > 6 ? "danger" : Number(avgHeat) > 3 ? "warning" : "success"}
          />
        </div>

        {/* Status filter tabs */}
        <div className="flex items-center gap-2 mb-4">
          {statusTabs.map((tab) => (
            <button
              key={tab.key}
              onClick={() => setStatusFilter(tab.key)}
              className={`px-4 py-2 rounded-xl text-sm font-medium transition-all duration-200 ${
                statusFilter === tab.key
                  ? "bg-accent text-white shadow-lg shadow-accent/25"
                  : "bg-card text-muted hover:text-foreground border border-border hover:border-accent/50"
              }`}
            >
              {tab.label}
              <span className="ml-1.5 opacity-70">
                ({statusCount(tab.key)})
              </span>
            </button>
          ))}
        </div>

        {/* Score filter tabs */}
        <div className="flex items-center gap-2 mb-6">
          {(
            [
              { key: "all", label: "All Scores" },
              { key: "high_risk", label: "High Risk" },
              { key: "hot", label: "Hot" },
            ] as const
          ).map((tab) => (
            <button
              key={tab.key}
              onClick={() => setFilter(tab.key)}
              className={`px-4 py-2 rounded-xl text-sm font-medium transition-all duration-200 ${
                filter === tab.key
                  ? "bg-accent/20 text-accent-light border border-accent/40"
                  : "bg-card text-muted hover:text-foreground border border-border hover:border-accent/50"
              }`}
            >
              {tab.label}
              {tab.key !== "all" && (
                <span className="ml-1.5 opacity-70">
                  (
                  {tab.key === "high_risk"
                    ? posts.filter((p) => p.risk_score >= 7).length
                    : posts.filter((p) => p.heat_score >= 7).length}
                  )
                </span>
              )}
            </button>
          ))}

          <button
            onClick={fetchPosts}
            className="ml-auto text-sm text-muted hover:text-accent-light bg-card border border-border rounded-xl px-4 py-2 hover:border-accent/50 transition-all"
          >
            Refresh
          </button>
        </div>

        {/* Posts list */}
        {loading ? (
          <div className="flex items-center justify-center h-64">
            <div className="w-8 h-8 border-2 border-accent border-t-transparent rounded-full animate-spin" />
          </div>
        ) : filteredPosts.length === 0 ? (
          <div className="glass-card rounded-2xl p-12 text-center">
            <p className="text-muted text-lg mb-2">No posts found</p>
            <p className="text-muted text-sm">
              Run <code className="bg-background px-2 py-1 rounded-lg border border-border">python main.py marketing</code> to analyze posts
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {filteredPosts.map((post) => (
              <PostCard key={post.id} post={post} onStatusChange={fetchPosts} />
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
