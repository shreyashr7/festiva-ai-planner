import { ShieldAlert, AlertTriangle, ChevronDown } from "lucide-react";
import * as Accordion from "@radix-ui/react-accordion";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { RiskItem } from "@/lib/types";
import { formatCurrency } from "@/lib/utils";

interface RiskSectionProps {
  risks: RiskItem[];
  contingency: number;
  totalBudget: number;
}

const IMPACT_VARIANT: Record<string, "danger" | "warning" | "info"> = {
  high: "danger",
  medium: "warning",
  low: "info",
};

export default function RiskSection({ risks, contingency, totalBudget }: RiskSectionProps) {
  return (
    <div className="space-y-4 animate-fade-in" style={{ animationDelay: "400ms" }}>
      <h2 className="text-xl font-semibold flex items-center gap-2">
        <ShieldAlert className="h-5 w-5 text-primary" />
        Risk Mitigation & Contingencies
      </h2>

      {/* Summary Cards */}
      <div className="grid grid-cols-2 gap-4">
        <Card className="border-border/50">
          <CardContent className="p-5 text-center">
            <div className="text-xs text-muted-foreground mb-1">Contingency Buffer (12%)</div>
            <div className="text-2xl font-bold text-amber-600">{formatCurrency(contingency)}</div>
          </CardContent>
        </Card>
        <Card className="border-border/50">
          <CardContent className="p-5 text-center">
            <div className="text-xs text-muted-foreground mb-1">Total with Contingency</div>
            <div className="text-2xl font-bold text-emerald-600">
              {formatCurrency(totalBudget + contingency)}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Risk Accordion */}
      <Card className="border-border/50">
        <CardContent className="p-0">
          <Accordion.Root type="multiple" defaultValue={["risk-0"]} className="divide-y divide-border">
            {risks.map((risk, i) => (
              <Accordion.Item key={risk.risk} value={`risk-${i}`}>
                <Accordion.Header>
                  <Accordion.Trigger className="flex w-full items-center justify-between px-5 py-4 text-left text-sm font-medium hover:bg-muted/50 transition-colors group cursor-pointer [&[data-state=open]>svg]:rotate-180">
                    <div className="flex items-center gap-3">
                      <AlertTriangle className="h-4 w-4 text-muted-foreground" />
                      <span>{risk.risk}</span>
                      <Badge variant={IMPACT_VARIANT[risk.impact] ?? "info"}>
                        {risk.impact}
                      </Badge>
                    </div>
                    <ChevronDown className="h-4 w-4 text-muted-foreground transition-transform duration-200" />
                  </Accordion.Trigger>
                </Accordion.Header>
                <Accordion.Content className="overflow-hidden data-[state=open]:animate-accordion-down data-[state=closed]:animate-accordion-up">
                  <div className="px-5 pb-4 pl-12 space-y-2">
                    <p className="text-sm text-muted-foreground leading-relaxed">
                      {risk.mitigation}
                    </p>
                    <div className="text-xs text-muted-foreground">
                      Recommended buffer:{" "}
                      <span className="font-semibold text-foreground">
                        {formatCurrency(risk.buffer)}
                      </span>
                    </div>
                  </div>
                </Accordion.Content>
              </Accordion.Item>
            ))}
          </Accordion.Root>
        </CardContent>
      </Card>
    </div>
  );
}
