import type { EventFormData, EventPlanResponse, HealthStatus } from "./types";

const API_BASE = "/api/v1";

class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = "ApiError";
  }
}

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${url}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new ApiError(res.status, (body as Record<string, string>).detail ?? "Request failed");
  }
  return res.json() as Promise<T>;
}

export async function checkHealth(): Promise<HealthStatus> {
  return request<HealthStatus>("/health");
}

export async function generatePlan(data: EventFormData): Promise<EventPlanResponse> {
  return request<EventPlanResponse>("/generate-plan", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export { ApiError };
