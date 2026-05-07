import type { EventFormData } from "./types";

const DEFAULTS: EventFormData = {
  event_type: "Wedding",
  guest_count: 300,
  total_budget: 2500000,
  event_month: new Date().getMonth() + 1,
  location: "Bengaluru",
};

const MONTH_MAP: Record<string, number> = {
  january: 1, jan: 1,
  february: 2, feb: 2,
  march: 3, mar: 3,
  april: 4, apr: 4,
  may: 5,
  june: 6, jun: 6,
  july: 7, jul: 7,
  august: 8, aug: 8,
  september: 9, sep: 9, sept: 9,
  october: 10, oct: 10,
  november: 11, nov: 11,
  december: 12, dec: 12,
};

const CITIES = [
  "bengaluru", "bangalore", "mumbai", "delhi", "hyderabad", "chennai",
  "kolkata", "pune", "ahmedabad", "jaipur", "goa", "kochi", "lucknow",
  "chandigarh", "udaipur", "mysore", "mysuru", "coorg", "ooty",
  "gurgaon", "noida", "indore", "bhopal", "nagpur", "vizag",
];

function parseEventType(input: string): EventFormData["event_type"] {
  const lower = input.toLowerCase();
  if (/\b(wedding|shaadi|marriage|nikah)\b/.test(lower)) return "Wedding";
  if (/\b(corporate|conference|office|company|business|seminar|summit)\b/.test(lower)) return "Corporate";
  if (/\b(birthday|bday|b'day)\b/.test(lower)) return "Birthday";
  return DEFAULTS.event_type;
}

function parseBudget(input: string): number {
  // Match patterns like: ₹10L, 10L, 10 lakhs, ₹10 lakh, 25L budget, budget 25L, 1500000, ₹15,00,000
  const patterns = [
    /(?:₹|rs\.?|inr)\s*([\d.]+)\s*(?:l|lakh|lakhs|lac)/i,
    /([\d.]+)\s*(?:l|lakh|lakhs|lac)/i,
    /(?:₹|rs\.?|inr)\s*([\d,.]+)\s*(?:cr|crore|crores)/i,
    /([\d.]+)\s*(?:cr|crore|crores)/i,
    /(?:₹|rs\.?|inr)\s*([\d,]+(?:\.\d+)?)\b/i,
    /budget\s*(?:of\s*)?(?:₹|rs\.?|inr)?\s*([\d,.]+)\s*(?:l|lakh|lakhs|lac)?/i,
  ];

  for (const pattern of patterns) {
    const match = input.match(pattern);
    if (match) {
      const raw = match[1].replace(/,/g, "");
      const num = parseFloat(raw);
      if (isNaN(num)) continue;

      // Determine multiplier from context
      const afterMatch = input.slice((match.index ?? 0) + match[0].length).toLowerCase();
      const fullMatch = match[0].toLowerCase();

      if (/cr|crore/.test(fullMatch)) return Math.min(Math.max(num * 10000000, 500000), 6000000);
      if (/l|lakh/.test(fullMatch)) return Math.min(Math.max(num * 100000, 500000), 6000000);
      if (/l|lakh/.test(afterMatch.slice(0, 10))) return Math.min(Math.max(num * 100000, 500000), 6000000);

      // If raw number is > 10000, assume it's already in INR
      if (num > 10000) return Math.min(Math.max(num, 500000), 6000000);
      // If small number, assume lakhs
      if (num <= 100) return Math.min(Math.max(num * 100000, 500000), 6000000);
      return Math.min(Math.max(num, 500000), 6000000);
    }
  }

  return DEFAULTS.total_budget;
}

function parseGuests(input: string): number {
  const patterns = [
    /([\d,]+)\s*(?:guests?|people|pax|persons?|attendees?)/i,
    /(?:guests?|people|pax|persons?|attendees?)\s*[:=]?\s*([\d,]+)/i,
    /(?:for|of)\s+([\d,]+)\s*(?:guests?|people|pax)?/i,
  ];

  for (const pattern of patterns) {
    const match = input.match(pattern);
    if (match) {
      const num = parseInt(match[1].replace(/,/g, ""), 10);
      if (!isNaN(num) && num >= 10 && num <= 5000) {
        return Math.min(Math.max(num, 100), 1200);
      }
    }
  }

  return DEFAULTS.guest_count;
}

function parseLocation(input: string): string {
  const lower = input.toLowerCase();

  // Try "in <city>" pattern
  const inMatch = lower.match(/\b(?:in|at|near)\s+([a-z]+(?:\s+[a-z]+)?)/);
  if (inMatch) {
    const candidate = inMatch[1].trim();
    for (const city of CITIES) {
      if (candidate.startsWith(city) || city.startsWith(candidate)) {
        return city.charAt(0).toUpperCase() + city.slice(1);
      }
    }
    // Return the matched word capitalized if it looks like a place
    if (!/wedding|corporate|birthday|budget|month|guest/.test(candidate)) {
      return candidate.charAt(0).toUpperCase() + candidate.slice(1);
    }
  }

  // Direct city mention
  for (const city of CITIES) {
    if (lower.includes(city)) {
      if (city === "bangalore" || city === "bengaluru") return "Bengaluru";
      return city.charAt(0).toUpperCase() + city.slice(1);
    }
  }

  return DEFAULTS.location;
}

function parseMonth(input: string): number {
  const lower = input.toLowerCase();
  for (const [name, num] of Object.entries(MONTH_MAP)) {
    if (lower.includes(name)) return num;
  }
  return DEFAULTS.event_month;
}

export function parseEventInput(input: string): EventFormData {
  return {
    event_type: parseEventType(input),
    total_budget: parseBudget(input),
    guest_count: parseGuests(input),
    location: parseLocation(input),
    event_month: parseMonth(input),
  };
}

export function describeDefaults(parsed: EventFormData, input: string): string[] {
  const hints: string[] = [];
  const lower = input.toLowerCase();

  if (!/wedding|shaadi|marriage|corporate|conference|office|birthday|bday/.test(lower)) {
    hints.push(`Event type: ${parsed.event_type} (default)`);
  }
  if (!/\d/.test(input) || (!/l|lakh|budget|₹|rs/i.test(lower) && !/guest|people|pax/.test(lower))) {
    // Check specifically for budget/guests
  }

  return hints;
}
