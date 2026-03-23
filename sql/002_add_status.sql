ALTER TABLE reddit_posts ADD COLUMN IF NOT EXISTS status text DEFAULT 'pending';
ALTER TABLE reddit_posts ADD COLUMN IF NOT EXISTS posted_at timestamptz;
CREATE INDEX IF NOT EXISTS idx_reddit_posts_status ON reddit_posts (status);
