CREATE TABLE IF NOT EXISTS farming_history (
    id serial PRIMARY KEY,
    post_id text,
    subreddit text,
    comment_id text,
    comment_text text,
    created_at timestamptz DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_farming_history_created ON farming_history (created_at DESC);
