import { createClient } from "@supabase/supabase-js";

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;

export const supabase = createClient(supabaseUrl, supabaseAnonKey);

export type RedditPost = {
  id: string;
  title: string;
  selftext: string;
  url: string;
  subreddit: string;
  score: number;
  num_comments: number;
  created_utc: number;
  title_ja: string;
  body_ja: string;
  risk_score: number;
  heat_score: number;
  reply_draft_en: string;
  reply_draft_ja: string;
  analyzed_at: string;
};
