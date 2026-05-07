import { Store, Star, MapPin, IndianRupee } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { VendorRecommendation } from "@/lib/types";
import { formatCurrency } from "@/lib/utils";

interface VendorCardsProps {
  vendors: VendorRecommendation[];
}

const CATEGORY_STYLES: Record<string, { badge: "default" | "info" | "warning"; border: string }> = {
  Venue: { badge: "info", border: "hover:border-blue-300" },
  Catering: { badge: "default", border: "hover:border-violet-300" },
  Decor: { badge: "warning", border: "hover:border-amber-300" },
};

export default function VendorCards({ vendors }: VendorCardsProps) {
  return (
    <div className="space-y-4 animate-fade-in" style={{ animationDelay: "300ms" }}>
      <h2 className="text-xl font-semibold flex items-center gap-2">
        <Store className="h-5 w-5 text-primary" />
        Vendor Recommendations
      </h2>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
        {vendors.map((v) => {
          const style = CATEGORY_STYLES[v.category] ?? { badge: "secondary" as const, border: "" };
          return (
            <Card
              key={`${v.name}-${v.category}`}
              className={`border-border/50 transition-all duration-200 ${style.border}`}
            >
              <CardContent className="p-5 space-y-3">
                <div className="flex items-start justify-between gap-2">
                  <Badge variant={style.badge}>{v.category}</Badge>
                  <div className="flex items-center gap-1 text-sm font-medium text-amber-600">
                    <Star className="h-3.5 w-3.5 fill-amber-400 text-amber-400" />
                    {v.rating}
                  </div>
                </div>

                <div>
                  <h3 className="text-sm font-semibold">{v.name}</h3>
                  <p className="mt-1 text-xs text-muted-foreground leading-relaxed">
                    {v.description}
                  </p>
                </div>

                <div className="flex items-center justify-between pt-2 border-t border-border/50">
                  <div className="flex items-center gap-1 text-xs text-muted-foreground">
                    <MapPin className="h-3 w-3" />
                    {v.location}
                  </div>
                  <div className="flex items-center gap-1 text-sm font-semibold text-primary">
                    <IndianRupee className="h-3.5 w-3.5" />
                    {formatCurrency(v.estimated_cost)}
                  </div>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
