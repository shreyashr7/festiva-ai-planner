import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, BarChart, Bar, XAxis, YAxis, CartesianGrid } from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { BarChart3 } from "lucide-react";
import type { BudgetAllocation } from "@/lib/types";
import { formatCurrency } from "@/lib/utils";

interface BudgetChartProps {
  budget: BudgetAllocation;
  guestCount: number;
}

const COLORS = ["#7c3aed", "#3b82f6", "#f43f5e"];

export default function BudgetChart({ budget, guestCount }: BudgetChartProps) {
  const pieData = [
    { name: "Catering", value: budget.catering_spend, pct: budget.catering_pct },
    { name: "Venue", value: budget.venue_spend, pct: budget.venue_pct },
    { name: "Decor", value: budget.decor_spend, pct: budget.decor_pct },
  ];

  const barData = [
    {
      name: "Catering",
      total: budget.catering_spend,
      perGuest: Math.round(budget.catering_spend / guestCount),
    },
    {
      name: "Venue",
      total: budget.venue_spend,
      perGuest: Math.round(budget.venue_spend / guestCount),
    },
    {
      name: "Decor",
      total: budget.decor_spend,
      perGuest: Math.round(budget.decor_spend / guestCount),
    },
  ];

  return (
    <div className="space-y-4 animate-fade-in" style={{ animationDelay: "100ms" }}>
      <h2 className="text-xl font-semibold flex items-center gap-2">
        <BarChart3 className="h-5 w-5 text-primary" />
        Budget Allocation
      </h2>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        {/* Donut Chart */}
        <Card className="border-border/50">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Distribution
            </CardTitle>
          </CardHeader>
          <CardContent className="pb-6">
            <div className="h-[280px]">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    innerRadius={70}
                    outerRadius={110}
                    paddingAngle={4}
                    dataKey="value"
                    stroke="none"
                  >
                    {pieData.map((_, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index]} />
                    ))}
                  </Pie>
                  <Tooltip
                    formatter={(value: number) => formatCurrency(value)}
                    contentStyle={{
                      borderRadius: "0.75rem",
                      border: "1px solid hsl(220 13% 91%)",
                      boxShadow: "0 4px 6px -1px rgb(0 0 0 / 0.05)",
                      fontSize: "0.875rem",
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
            {/* Legend */}
            <div className="flex justify-center gap-6 mt-2">
              {pieData.map((entry, i) => (
                <div key={entry.name} className="flex items-center gap-2 text-sm">
                  <div className="h-3 w-3 rounded-full" style={{ backgroundColor: COLORS[i] }} />
                  <span className="text-muted-foreground">{entry.name}</span>
                  <span className="font-semibold">{entry.pct}%</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Bar Chart */}
        <Card className="border-border/50">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Per-Guest Cost Comparison
            </CardTitle>
          </CardHeader>
          <CardContent className="pb-6">
            <div className="h-[280px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={barData} barCategoryGap="20%">
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(220 13% 91%)" />
                  <XAxis
                    dataKey="name"
                    tick={{ fontSize: 12, fill: "hsl(220 9% 46%)" }}
                    axisLine={false}
                    tickLine={false}
                  />
                  <YAxis
                    tick={{ fontSize: 12, fill: "hsl(220 9% 46%)" }}
                    axisLine={false}
                    tickLine={false}
                    tickFormatter={(v: number) => `₹${(v / 1000).toFixed(0)}K`}
                  />
                  <Tooltip
                    formatter={(value: number) => [`₹${value.toLocaleString("en-IN")}`, "Per Guest"]}
                    contentStyle={{
                      borderRadius: "0.75rem",
                      border: "1px solid hsl(220 13% 91%)",
                      boxShadow: "0 4px 6px -1px rgb(0 0 0 / 0.05)",
                      fontSize: "0.875rem",
                    }}
                  />
                  <Bar dataKey="perGuest" radius={[6, 6, 0, 0]}>
                    {barData.map((_, index) => (
                      <Cell key={`bar-${index}`} fill={COLORS[index]} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
            {/* Per-guest summary */}
            <div className="mt-4 flex justify-center gap-6">
              {barData.map((entry, i) => (
                <div key={entry.name} className="text-center">
                  <div className="text-xs text-muted-foreground">{entry.name}</div>
                  <div className="text-sm font-semibold" style={{ color: COLORS[i] }}>
                    ₹{entry.perGuest.toLocaleString("en-IN")}/guest
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
