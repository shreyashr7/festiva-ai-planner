import { Clock, Building, Palette, Settings, PartyPopper, Check } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import type { TimelineWeek } from "@/lib/types";

interface TimelineSectionProps {
  timeline: TimelineWeek[];
}

const ICON_MAP: Record<string, React.ElementType> = {
  building: Building,
  palette: Palette,
  settings: Settings,
  "party-popper": PartyPopper,
};

const STEP_COLORS = [
  "border-violet-500 bg-violet-50",
  "border-blue-500 bg-blue-50",
  "border-amber-500 bg-amber-50",
  "border-emerald-500 bg-emerald-50",
];

const DOT_COLORS = [
  "bg-violet-500",
  "bg-blue-500",
  "bg-amber-500",
  "bg-emerald-500",
];

export default function TimelineSection({ timeline }: TimelineSectionProps) {
  return (
    <div className="space-y-4 animate-fade-in" style={{ animationDelay: "200ms" }}>
      <h2 className="text-xl font-semibold flex items-center gap-2">
        <Clock className="h-5 w-5 text-primary" />
        6-Week Implementation Timeline
      </h2>

      <div className="relative space-y-4 pl-8">
        {/* Vertical line */}
        <div className="absolute left-[15px] top-2 bottom-2 w-px bg-border" />

        {timeline.map((week, i) => {
          const Icon = ICON_MAP[week.icon] ?? Clock;
          return (
            <div key={week.week} className="relative">
              {/* Dot */}
              <div
                className={`absolute -left-8 top-5 h-[11px] w-[11px] rounded-full ring-4 ring-background ${DOT_COLORS[i % DOT_COLORS.length]}`}
              />

              <Card className={`border-l-4 ${STEP_COLORS[i % STEP_COLORS.length]} border-border/50`}>
                <CardContent className="p-5">
                  <div className="flex items-start justify-between gap-4 mb-3">
                    <div className="flex items-center gap-3">
                      <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-white shadow-sm">
                        <Icon className="h-4 w-4 text-muted-foreground" />
                      </div>
                      <div>
                        <div className="text-sm font-semibold">{week.week}</div>
                        <div className="text-xs text-muted-foreground">{week.phase}</div>
                      </div>
                    </div>
                    <span className="rounded-md bg-white px-2.5 py-1 text-xs font-medium text-muted-foreground shadow-sm whitespace-nowrap">
                      {week.budget_note}
                    </span>
                  </div>

                  <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
                    {week.tasks.map((task) => (
                      <div key={task} className="flex items-start gap-2 text-sm text-muted-foreground">
                        <Check className="mt-0.5 h-3.5 w-3.5 shrink-0 text-emerald-500" />
                        <span>{task}</span>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          );
        })}
      </div>
    </div>
  );
}
