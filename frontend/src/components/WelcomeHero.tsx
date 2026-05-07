import {
  Sparkles,
  TrendingUp,
  MapPin,
  BarChart3,
  Clock,
  Download,
} from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";

const features = [
  {
    icon: TrendingUp,
    title: "Budget Intelligence",
    description: "ML-powered spending predictions based on Bengaluru market rates",
    color: "text-violet-600 bg-violet-100",
  },
  {
    icon: BarChart3,
    title: "Visual Analytics",
    description: "Interactive charts and metrics for budget allocation breakdown",
    color: "text-blue-600 bg-blue-100",
  },
  {
    icon: Clock,
    title: "6-Week Timeline",
    description: "Week-by-week implementation plan with milestone tracking",
    color: "text-emerald-600 bg-emerald-100",
  },
  {
    icon: MapPin,
    title: "Venue Intelligence",
    description: "AI-curated Bengaluru venue recommendations from knowledge base",
    color: "text-amber-600 bg-amber-100",
  },
  {
    icon: Sparkles,
    title: "Smart Vendors",
    description: "Cost-matched vendor recommendations with ratings and reviews",
    color: "text-rose-600 bg-rose-100",
  },
  {
    icon: Download,
    title: "Export Ready",
    description: "Download professional reports in Markdown or JSON format",
    color: "text-cyan-600 bg-cyan-100",
  },
];

const budgetRanges = [
  { type: "🎂 Birthday", min: "₹5L", typical: "₹15L", max: "₹25L" },
  { type: "💼 Corporate", min: "₹10L", typical: "₹30L", max: "₹60L" },
  { type: "💒 Wedding", min: "₹15L", typical: "₹35L", max: "₹60L" },
];

export default function WelcomeHero() {
  return (
    <div className="space-y-8 animate-fade-in">
      {/* Hero */}
      <div className="text-center space-y-4 py-8">
        <div className="inline-flex items-center gap-2 rounded-full bg-primary/10 px-4 py-1.5 text-sm font-medium text-primary">
          <Sparkles className="h-4 w-4" />
          AI-Powered Event Planning
        </div>
        <h1 className="text-4xl font-bold tracking-tight text-foreground sm:text-5xl">
          Plan your perfect event
          <br />
          <span className="bg-gradient-to-r from-violet-600 to-purple-600 bg-clip-text text-transparent">
            in minutes, not months
          </span>
        </h1>
        <p className="mx-auto max-w-2xl text-lg text-muted-foreground">
          Configure your event in the sidebar, hit generate, and get a complete plan with
          budget breakdowns, vendor recommendations, and a 6-week timeline.
        </p>
      </div>

      {/* Feature Grid */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {features.map((f) => (
          <Card key={f.title} className="group border-border/50 hover:border-primary/30 transition-all duration-300">
            <CardContent className="p-5 flex gap-4">
              <div className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-lg ${f.color}`}>
                <f.icon className="h-5 w-5" />
              </div>
              <div>
                <h3 className="text-sm font-semibold">{f.title}</h3>
                <p className="mt-1 text-xs text-muted-foreground leading-relaxed">{f.description}</p>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Budget Ranges Table */}
      <Card className="border-border/50">
        <CardContent className="p-6">
          <h3 className="text-sm font-semibold mb-4 text-muted-foreground uppercase tracking-wider">
            Bengaluru Event Budget Ranges
          </h3>
          <div className="overflow-hidden rounded-lg border border-border">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-muted/50">
                  <th className="px-4 py-3 text-left font-medium text-muted-foreground">Event Type</th>
                  <th className="px-4 py-3 text-right font-medium text-muted-foreground">Min</th>
                  <th className="px-4 py-3 text-right font-medium text-muted-foreground">Typical</th>
                  <th className="px-4 py-3 text-right font-medium text-muted-foreground">Max</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border">
                {budgetRanges.map((r) => (
                  <tr key={r.type} className="hover:bg-muted/30 transition-colors">
                    <td className="px-4 py-3 font-medium">{r.type}</td>
                    <td className="px-4 py-3 text-right text-muted-foreground">{r.min}</td>
                    <td className="px-4 py-3 text-right font-semibold text-primary">{r.typical}</td>
                    <td className="px-4 py-3 text-right text-muted-foreground">{r.max}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
