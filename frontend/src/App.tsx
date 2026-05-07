import { useState, useEffect, useCallback } from "react";
import Header from "@/components/Header";
import EventForm from "@/components/EventForm";
import WelcomeHero from "@/components/WelcomeHero";
import BudgetOverview from "@/components/BudgetOverview";
import BudgetChart from "@/components/BudgetChart";
import TimelineSection from "@/components/TimelineSection";
import VendorCards from "@/components/VendorCards";
import RiskSection from "@/components/RiskSection";
import ExportSection from "@/components/ExportSection";
import { Separator } from "@/components/ui/separator";
import { checkHealth, generatePlan, ApiError } from "@/lib/api";
import type { EventFormData, EventPlanResponse } from "@/lib/types";

export default function App() {
  const [apiStatus, setApiStatus] = useState<"connected" | "offline" | "checking">("checking");
  const [formData, setFormData] = useState<EventFormData>({
    event_type: "Wedding",
    guest_count: 500,
    total_budget: 2500000,
    event_month: 5,
    location: "Bengaluru",
  });
  const [loading, setLoading] = useState(false);
  const [plan, setPlan] = useState<EventPlanResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Health check on mount
  useEffect(() => {
    let cancelled = false;
    async function check() {
      try {
        await checkHealth();
        if (!cancelled) setApiStatus("connected");
      } catch {
        if (!cancelled) setApiStatus("offline");
      }
    }
    check();
    const interval = setInterval(check, 30_000);
    return () => {
      cancelled = true;
      clearInterval(interval);
    };
  }, []);

  const handleSubmit = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await generatePlan(formData);
      setPlan(result);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError("Failed to connect to the API server. Make sure it's running.");
      }
    } finally {
      setLoading(false);
    }
  }, [formData]);

  return (
    <div className="min-h-screen bg-background">
      <Header apiStatus={apiStatus} />

      <div className="mx-auto max-w-[1440px] px-6 py-6">
        <div className="flex gap-6 items-start">
          {/* Sidebar - Form */}
          <aside className="w-[340px] shrink-0 hidden lg:block">
            <EventForm
              data={formData}
              onChange={setFormData}
              onSubmit={handleSubmit}
              loading={loading}
            />
          </aside>

          {/* Mobile form */}
          <div className="lg:hidden w-full mb-6">
            <EventForm
              data={formData}
              onChange={setFormData}
              onSubmit={handleSubmit}
              loading={loading}
            />
          </div>

          {/* Main Content */}
          <main className="flex-1 min-w-0 space-y-8">
            {error && (
              <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700 animate-fade-in">
                <strong>Error:</strong> {error}
              </div>
            )}

            {!plan && !loading && <WelcomeHero />}

            {plan && (
              <>
                {/* Event header */}
                <div className="flex items-center gap-4 animate-fade-in">
                  <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-violet-500 to-purple-600 text-2xl shadow-lg">
                    {plan.event_type === "Wedding" && "💒"}
                    {plan.event_type === "Corporate" && "💼"}
                    {plan.event_type === "Birthday" && "🎂"}
                  </div>
                  <div>
                    <h1 className="text-2xl font-bold">
                      {plan.event_type} Event Plan
                    </h1>
                    <p className="text-sm text-muted-foreground">
                      {plan.guest_count} guests · {plan.location} · Generated{" "}
                      {new Date(plan.generated_at).toLocaleString()}
                    </p>
                  </div>
                </div>

                <Separator />
                <BudgetOverview plan={plan} />
                <Separator />
                <BudgetChart budget={plan.budget_allocation} guestCount={plan.guest_count} />
                <Separator />
                <TimelineSection timeline={plan.timeline} />
                <Separator />
                <VendorCards vendors={plan.vendors} />
                <Separator />
                <RiskSection
                  risks={plan.risks}
                  contingency={plan.contingency_budget}
                  totalBudget={plan.total_budget}
                />
                <Separator />
                <ExportSection plan={plan} />

                {/* Footer */}
                <div className="py-8 text-center text-xs text-muted-foreground">
                  Festiva AI · Premium Event Planning for Bengaluru · Powered by Machine Learning
                </div>
              </>
            )}
          </main>
        </div>
      </div>
    </div>
  );
}
