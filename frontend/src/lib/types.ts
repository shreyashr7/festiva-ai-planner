export interface BudgetAllocation {
  event_type: string;
  guest_count: number;
  total_budget: number;
  catering_spend: number;
  venue_spend: number;
  decor_spend: number;
  catering_pct: number;
  venue_pct: number;
  decor_pct: number;
}

export interface TimelineWeek {
  week: string;
  phase: string;
  icon: string;
  tasks: string[];
  budget_note: string;
}

export interface VendorRecommendation {
  name: string;
  category: string;
  estimated_cost: number;
  rating: number;
  description: string;
  location: string;
}

export interface RiskItem {
  risk: string;
  impact: string;
  mitigation: string;
  buffer: number;
}

export interface EventPlanResponse {
  status: string;
  request_id: string;
  event_type: string;
  guest_count: number;
  total_budget: number;
  location: string;
  event_month: number;
  budget_allocation: BudgetAllocation;
  per_guest_cost: number;
  contingency_budget: number;
  timeline: TimelineWeek[];
  vendors: VendorRecommendation[];
  risks: RiskItem[];
  recommendations: string;
  generated_at: string;
}

export interface EventFormData {
  event_type: "Wedding" | "Corporate" | "Birthday";
  guest_count: number;
  total_budget: number;
  event_month: number;
  location: string;
}

export interface HealthStatus {
  status: string;
  timestamp: string;
  service: string;
}
