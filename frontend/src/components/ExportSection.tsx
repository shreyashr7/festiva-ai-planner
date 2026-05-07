import { Download, FileText, FileJson } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import type { EventPlanResponse } from "@/lib/types";

interface ExportSectionProps {
  plan: EventPlanResponse;
}

function downloadFile(content: string, filename: string, mime: string) {
  const blob = new Blob([content], { type: mime });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

export default function ExportSection({ plan }: ExportSectionProps) {
  const dateStr = new Date().toISOString().slice(0, 10);

  function handleMarkdown() {
    downloadFile(
      plan.recommendations,
      `festiva_plan_${plan.event_type.toLowerCase()}_${dateStr}.md`,
      "text/markdown",
    );
  }

  function handleJson() {
    const data = {
      event_type: plan.event_type,
      guest_count: plan.guest_count,
      total_budget: plan.total_budget,
      location: plan.location,
      event_month: plan.event_month,
      budget_allocation: plan.budget_allocation,
      per_guest_cost: plan.per_guest_cost,
      contingency_budget: plan.contingency_budget,
      timeline: plan.timeline,
      vendors: plan.vendors,
      risks: plan.risks,
      generated_at: plan.generated_at,
    };
    downloadFile(
      JSON.stringify(data, null, 2),
      `festiva_plan_${plan.event_type.toLowerCase()}_${dateStr}.json`,
      "application/json",
    );
  }

  return (
    <div className="space-y-4 animate-fade-in" style={{ animationDelay: "500ms" }}>
      <h2 className="text-xl font-semibold flex items-center gap-2">
        <Download className="h-5 w-5 text-primary" />
        Export Report
      </h2>

      <Card className="border-border/50">
        <CardContent className="p-5">
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
            <Button variant="outline" size="lg" onClick={handleMarkdown} className="justify-start gap-3">
              <FileText className="h-5 w-5 text-violet-500" />
              <div className="text-left">
                <div className="text-sm font-medium">Download Markdown</div>
                <div className="text-xs text-muted-foreground">Human-readable report</div>
              </div>
            </Button>
            <Button variant="outline" size="lg" onClick={handleJson} className="justify-start gap-3">
              <FileJson className="h-5 w-5 text-blue-500" />
              <div className="text-left">
                <div className="text-sm font-medium">Download JSON</div>
                <div className="text-xs text-muted-foreground">Machine-readable data</div>
              </div>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
