"use client";

type StatsCardProps = {
  label: string;
  value: string | number;
  sub?: string;
  icon: React.ReactNode;
  color: "accent" | "success" | "warning" | "danger";
};

const colorMap = {
  accent: "text-accent-light bg-accent/10 glow-accent",
  success: "text-success bg-success/10 glow-success",
  warning: "text-warning bg-warning/10 glow-warning",
  danger: "text-danger bg-danger/10 glow-danger",
};

const valueColorMap = {
  accent: "text-accent-light",
  success: "text-success",
  warning: "text-warning",
  danger: "text-danger",
};

export default function StatsCard({ label, value, sub, icon, color }: StatsCardProps) {
  return (
    <div className="glass-card rounded-2xl p-6 hover:bg-card-hover transition-all duration-300 group">
      <div className="flex items-start justify-between mb-4">
        <div className={`p-3 rounded-xl ${colorMap[color]}`}>{icon}</div>
      </div>
      <p className="text-muted text-sm mb-1">{label}</p>
      <p className={`text-3xl font-bold ${valueColorMap[color]}`}>{value}</p>
      {sub && <p className="text-muted text-xs mt-1">{sub}</p>}
    </div>
  );
}
