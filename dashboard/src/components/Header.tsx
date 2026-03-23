"use client";

import { supabase } from "@/lib/supabase";
import { useRouter } from "next/navigation";
import type { User } from "@supabase/supabase-js";

export default function Header({ user }: { user: User | null }) {
  const router = useRouter();

  const handleLogout = async () => {
    await supabase.auth.signOut();
    router.push("/login");
    router.refresh();
  };

  return (
    <header className="sticky top-0 z-50 glass-card border-b border-border">
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <h1 className="text-xl font-bold gradient-text">MVMNT</h1>
          <span className="text-xs text-muted bg-background border border-border rounded-full px-3 py-1">
            Reddit Intelligence
          </span>
        </div>
        <div className="flex items-center gap-4">
          {user && (
            <>
              <span className="text-sm text-muted">{user.email}</span>
              <button
                onClick={handleLogout}
                className="text-sm text-muted hover:text-foreground bg-background border border-border rounded-xl px-4 py-2 hover:border-accent/50 transition-all"
              >
                Logout
              </button>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
