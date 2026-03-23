"use client";

type Props = {
  score: number;
  label?: string;
};

export default function RiskBadge({ score, label }: Props) {
  const getColor = (s: number) => {
    if (s <= 3) return { bg: "bg-success/15", text: "text-success", ring: "ring-success/30" };
    if (s <= 6) return { bg: "bg-warning/15", text: "text-warning", ring: "ring-warning/30" };
    return { bg: "bg-danger/15", text: "text-danger", ring: "ring-danger/30" };
  };

  const c = getColor(score);

  return (
    <span
      className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold ring-1 ${c.bg} ${c.text} ${c.ring}`}
    >
      {label && <span className="opacity-70">{label}</span>}
      {score}/10
    </span>
  );
}
