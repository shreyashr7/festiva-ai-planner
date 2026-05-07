import { IndianRupee, Users, TrendingUp, ShieldCheck } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import type { EventPlanResponse } from "@/lib/types";
import { formatCurrency } from "@/lib/utils";

interface BudgetOverviewProps {
  plan: EventPlanResponse;
}

export default function BudgetOverview({ plan }: BudgetOverviewProps) {
  const b = plan.budget_allocation;
  const cards = [
    {
      label: "Total Budget",
      value: formatCurrency(plan.total_budget),
      sub: `${plan.event_type} Event`,
      icon: IndianRupee,
      color: "text-violet-600 bg-violet-100",
    },
    {
      label: "Per Guest Cost",
      value: formatCurrency(plan.per_guest_cost),
      sub: `${plan.guest_count} guests`,
      icon: Users,
      color: "text-blue-600 bg-blue-100",
    },
    {
      label: "Contingency (12%)",
      value: formatCurrency(plan.contingency_budget),
      sub: "Buffer reserve",
      icon: ShieldCheck,
      color: "text-amber-600 bg-amber-100",
    },
    {
      label: "With Contingency",
      value: formatCurrency(plan.total_budget + plan.contingency_budget),
      sub: "Total recommended",
      icon: TrendingUp,
      color: "text-emerald-600 bg-emerald-100",
    },
  ];

  return (
    <div className="space-y-4 animate-fade-in">
      <h2 className="text-xl font-semibold flex items-center gap-2">
        <IndianRupee className="h-5 w-5 text-primary" />
        Financial Summary
      </h2>

      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        {cards.map((c) => (
          <Card key={c.label} className="border-border/50">
            <CardContent className="p-5">
              <div className="flex items-center gap-3 mb-3">
                <div className={`flex h-9 w-9 items-center justify-center rounded-lg ${c.color}`}>
                  <c.icon className="h-4 w-4" />
                </div>
                <span className="text-xs font-medium text-muted-foreground">{c.label}</span>
              </div>
              <div className="text-2xl font-bold tracking-tight">{c.value}</div>
              <div className="mt-1 text-xs text-muted-foreground">{c.sub}</div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Category Bars */}
      <Card className="border-border/50">
        <CardContent className="p-5 space-y-4">
          {[
            { label: "Catering", pct: b.catering_pct, spend: b.catering_spend, color: "bg-violet-500" },
            { label: "Venue", pct: b.venue_pct, spend: b.venue_spend, color: "bg-blue-500" },
            { label: "Decor", pct: b.decor_pct, spend: b.decor_spend, color: "bg-rose-500" },
          ].map((cat) => (
            <div key={cat.label} className="space-y-1.5">
              <div className="flex items-center justify-between text-sm">
                <span className="font-medium">{cat.label}</span>
                <span className="text-muted-foreground">
                  {formatCurrency(cat.spend)}{" "}
                  <span className="text-xs">({cat.pct}%)</span>
                </span>
              </div>
              <div className="h-2.5 w-full overflow-hidden rounded-full bg-secondary">
                <div
                  className={`h-full rounded-full ${cat.color} transition-all duration-700 ease-out`}
                  style={{ width: `${cat.pct}%` }}
                />
              </div>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  );
}
