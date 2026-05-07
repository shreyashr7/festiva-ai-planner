import { useState } from "react";
import {
  Sparkles,
  Send,
  IndianRupee,
  Users,
  MapPin,
  CalendarDays,
  PartyPopper,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import type { EventFormData } from "@/lib/types";
import { parseEventInput } from "@/lib/parser";
import { formatCurrency, MONTH_NAMES } from "@/lib/utils";

interface EventFormProps {
  onSubmit: (data: EventFormData) => void;
  loading: boolean;
}

const EXAMPLES = [
  "Wedding in Bangalore, budget ₹10L",
  "Corporate event, 200 guests, ₹15L, December",
  "Birthday party in Mumbai, 50 guests, budget ₹5L",
  "Grand wedding, 800 guests, ₹40L, Hyderabad, February",
];

export default function EventForm({ onSubmit, loading }: EventFormProps) {
  const [input, setInput] = useState("");
  const [parsed, setParsed] = useState<EventFormData | null>(null);

  function handleInputChange(value: string) {
    setInput(value);
    if (value.trim().length > 3) {
      setParsed(parseEventInput(value));
    } else {
      setParsed(null);
    }
  }

  function handleSubmit() {
    if (!input.trim()) return;
    const data = parseEventInput(input);
    onSubmit(data);
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  }

  function handleExample(example: string) {
    setInput(example);
    setParsed(parseEventInput(example));
  }

  return (
    <Card className="sticky top-6 border-border/60 bg-white/80 backdrop-blur-sm">
      <CardContent className="p-6 space-y-5">
        {/* Header */}
        <div className="flex items-center gap-3 pb-1">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10">
            <Sparkles className="h-5 w-5 text-primary" />
          </div>
          <div>
            <h2 className="text-base font-semibold">Plan Your Event</h2>
            <p className="text-xs text-muted-foreground">Describe your event in plain English</p>
          </div>
        </div>

        {/* Text Input */}
        <div className="space-y-2">
          <div className="relative">
            <textarea
              value={input}
              onChange={(e) => handleInputChange(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Wedding in Bangalore, budget ₹10L, 300 guests, December"
              rows={3}
              className="w-full resize-none rounded-xl border border-input bg-background px-4 py-3 pr-12 text-sm leading-relaxed placeholder:text-muted-foreground/60 focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary/40"
            />
            <button
              onClick={handleSubmit}
              disabled={loading || !input.trim()}
              className="absolute bottom-3 right-3 flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground transition-all hover:bg-primary/90 disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer"
            >
              <Send className="h-4 w-4" />
            </button>
          </div>
          <p className="text-[11px] text-muted-foreground">
            Press <kbd className="rounded border border-border px-1 py-0.5 text-[10px] font-mono">Enter</kbd> to generate
          </p>
        </div>

        {/* Examples */}
        <div className="space-y-2">
          <p className="text-xs font-medium text-muted-foreground">Try an example:</p>
          <div className="flex flex-wrap gap-1.5">
            {EXAMPLES.map((ex) => (
              <button
                key={ex}
                onClick={() => handleExample(ex)}
                className="rounded-lg border border-border/60 bg-secondary/50 px-2.5 py-1.5 text-[11px] text-muted-foreground transition-all hover:bg-primary/10 hover:text-primary hover:border-primary/30 cursor-pointer"
              >
                {ex}
              </button>
            ))}
          </div>
        </div>

        {/* Live Parse Preview */}
        {parsed && (
          <div className="space-y-2 rounded-xl border border-primary/20 bg-primary/[0.03] p-4 animate-fade-in">
            <p className="text-xs font-semibold text-primary flex items-center gap-1.5">
              <Sparkles className="h-3 w-3" />
              Parsed from your input
            </p>
            <div className="grid grid-cols-2 gap-2 text-xs">
              <div className="flex items-center gap-1.5">
                <PartyPopper className="h-3 w-3 text-muted-foreground" />
                <span className="text-muted-foreground">Type:</span>
                <span className="font-medium">{parsed.event_type}</span>
              </div>
              <div className="flex items-center gap-1.5">
                <IndianRupee className="h-3 w-3 text-muted-foreground" />
                <span className="text-muted-foreground">Budget:</span>
                <span className="font-medium">{formatCurrency(parsed.total_budget)}</span>
              </div>
              <div className="flex items-center gap-1.5">
                <Users className="h-3 w-3 text-muted-foreground" />
                <span className="text-muted-foreground">Guests:</span>
                <span className="font-medium">{parsed.guest_count}</span>
              </div>
              <div className="flex items-center gap-1.5">
                <MapPin className="h-3 w-3 text-muted-foreground" />
                <span className="text-muted-foreground">City:</span>
                <span className="font-medium">{parsed.location}</span>
              </div>
              <div className="flex items-center gap-1.5 col-span-2">
                <CalendarDays className="h-3 w-3 text-muted-foreground" />
                <span className="text-muted-foreground">Month:</span>
                <span className="font-medium">{MONTH_NAMES[parsed.event_month - 1]}</span>
              </div>
            </div>
          </div>
        )}

        {/* Submit */}
        <Button
          onClick={handleSubmit}
          disabled={loading || !input.trim()}
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
