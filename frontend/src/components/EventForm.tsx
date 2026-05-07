import {
  Sparkles,
  IndianRupee,
  Users,
  MapPin,
  CalendarDays,
  ChevronDown,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import type { EventFormData } from "@/lib/types";
import { MONTH_NAMES, formatCurrency } from "@/lib/utils";

interface EventFormProps {
  data: EventFormData;
  onChange: (data: EventFormData) => void;
  onSubmit: () => void;
  loading: boolean;
}

const EVENT_TYPES = ["Wedding", "Corporate", "Birthday"] as const;

export default function EventForm({ data, onChange, onSubmit, loading }: EventFormProps) {
  return (
    <Card className="sticky top-6 border-border/60 bg-white/80 backdrop-blur-sm">
      <CardContent className="p-6 space-y-6">
        {/* Header */}
        <div className="flex items-center gap-3 pb-2">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10">
            <Sparkles className="h-5 w-5 text-primary" />
          </div>
          <div>
            <h2 className="text-base font-semibold">Event Configuration</h2>
            <p className="text-xs text-muted-foreground">Configure your event details</p>
          </div>
        </div>

        {/* Event Type */}
        <div className="space-y-2">
          <label className="text-sm font-medium flex items-center gap-1.5">
            <CalendarDays className="h-3.5 w-3.5 text-muted-foreground" />
            Event Type
          </label>
          <div className="grid grid-cols-3 gap-2">
            {EVENT_TYPES.map((type) => (
              <button
                key={type}
                onClick={() => onChange({ ...data, event_type: type })}
                className={`rounded-lg px-3 py-2.5 text-sm font-medium transition-all duration-200 cursor-pointer ${
                  data.event_type === type
                    ? "bg-primary text-primary-foreground shadow-md scale-[1.02]"
                    : "bg-secondary text-secondary-foreground hover:bg-secondary/80"
                }`}
              >
                {type === "Wedding" && "💒"}
                {type === "Corporate" && "💼"}
                {type === "Birthday" && "🎂"}{" "}
                {type}
              </button>
            ))}
          </div>
        </div>

        {/* Guest Count */}
        <div className="space-y-2">
          <label className="text-sm font-medium flex items-center justify-between">
            <span className="flex items-center gap-1.5">
              <Users className="h-3.5 w-3.5 text-muted-foreground" />
              Guests
            </span>
            <span className="text-primary font-semibold">{data.guest_count}</span>
          </label>
          <input
            type="range"
            min={100}
            max={1200}
            step={50}
            value={data.guest_count}
            onChange={(e) => onChange({ ...data, guest_count: Number(e.target.value) })}
            className="w-full h-2 rounded-full appearance-none bg-secondary accent-primary cursor-pointer"
          />
          <div className="flex justify-between text-[11px] text-muted-foreground">
            <span>100</span>
            <span>600</span>
            <span>1200</span>
          </div>
        </div>

        {/* Budget */}
        <div className="space-y-2">
          <label className="text-sm font-medium flex items-center justify-between">
            <span className="flex items-center gap-1.5">
              <IndianRupee className="h-3.5 w-3.5 text-muted-foreground" />
              Budget
            </span>
            <span className="text-primary font-semibold">{formatCurrency(data.total_budget)}</span>
          </label>
          <input
            type="range"
            min={500000}
            max={6000000}
            step={100000}
            value={data.total_budget}
            onChange={(e) => onChange({ ...data, total_budget: Number(e.target.value) })}
            className="w-full h-2 rounded-full appearance-none bg-secondary accent-primary cursor-pointer"
          />
          <div className="flex justify-between text-[11px] text-muted-foreground">
            <span>₹5L</span>
            <span>₹30L</span>
            <span>₹60L</span>
          </div>
        </div>

        {/* Month */}
        <div className="space-y-2">
          <label className="text-sm font-medium flex items-center gap-1.5">
            <CalendarDays className="h-3.5 w-3.5 text-muted-foreground" />
            Event Month
          </label>
          <div className="relative">
            <select
              value={data.event_month}
              onChange={(e) => onChange({ ...data, event_month: Number(e.target.value) })}
              className="w-full appearance-none rounded-lg border border-input bg-background px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-ring cursor-pointer"
            >
              {MONTH_NAMES.map((name, i) => (
                <option key={i} value={i + 1}>
                  {name}
                </option>
              ))}
            </select>
            <ChevronDown className="pointer-events-none absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          </div>
        </div>

        {/* Location */}
        <div className="space-y-2">
          <label className="text-sm font-medium flex items-center gap-1.5">
            <MapPin className="h-3.5 w-3.5 text-muted-foreground" />
            Location
          </label>
          <input
            type="text"
            value={data.location}
            onChange={(e) => onChange({ ...data, location: e.target.value })}
            placeholder="Bengaluru"
            className="w-full rounded-lg border border-input bg-background px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
          />
        </div>

        {/* Submit */}
        <Button
          onClick={onSubmit}
          disabled={loading}
          size="lg"
          className="w-full text-base font-semibold"
        >
          {loading ? (
            <>
              <svg className="h-5 w-5 animate-spin" viewBox="0 0 24 24" fill="none">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              Generating Plan…
            </>
          ) : (
            <>
              <Sparkles className="h-5 w-5" />
              Generate Event Plan
            </>
          )}
        </Button>
      </CardContent>
    </Card>
  );
}
