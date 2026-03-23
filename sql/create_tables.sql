-- reddit_posts table for storing analyzed Reddit posts
-- Run this in the Supabase SQL Editor (https://supabase.com/dashboard → SQL Editor)

create table if not exists reddit_posts (
    id              text        primary key,   -- Reddit post ID (e.g. "t3_abc123")
    title           text,
    selftext        text,
    url             text,
    subreddit       text,
    score           integer,
    num_comments    integer,
    created_utc     double precision,          -- Reddit epoch timestamp
    title_ja        text,
    body_ja         text,
    risk_score      real,
    heat_score      real,
    reply_draft_en  text,
    reply_draft_ja  text,
    analyzed_at     timestamptz default now()
);

-- Index for the most common query pattern (recent posts)
create index if not exists idx_reddit_posts_analyzed_at
    on reddit_posts (analyzed_at desc);

-- Optional: enable Row Level Security (recommended for production)
-- alter table reddit_posts enable row level security;
