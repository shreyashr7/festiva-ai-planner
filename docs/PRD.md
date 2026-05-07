# Festiva Planner AI
## Product Requirements Document

**Version:** 1.0
**Status:** Draft Requirements
**Last Updated:** May 7, 2026
**Product Type:** AI-powered event planning assistant
**Target Market:** Bengaluru, India

---

## 1. Purpose

Festiva Planner AI will be an intelligent event planning platform that will help users plan weddings, corporate events, and birthday celebrations through automated budget allocation, vendor discovery, knowledge retrieval, and multi-agent planning.

The product will be designed as a future-state system. This document will describe what the platform will do, how it will behave, and what each feature must accomplish once implemented.

---

## 2. Product Vision

The product will allow a user to describe an event in natural language or structured form, and the system will then generate a complete event plan that will include:

- Budget breakdowns
- Event timelines
- Task checklists
- Vendor recommendations
- Risk mitigation notes
- Downloadable planning outputs

The platform will combine machine learning, retrieval-augmented generation, and multi-agent orchestration to reduce planning effort and improve decision quality.

---

## 3. Objectives

The system will:

- Understand event requirements from user input
- Predict budget allocation for major event categories
- Retrieve relevant planning knowledge and vendor guidance
- Generate a professional event plan with timelines and tasks
- Recommend vendors that match budget and event type
- Provide a dashboard for planning, review, and export
- Support a future LLM-driven agent workflow for reasoning and explanation

---

## 4. Scope

### In Scope
The first release will support:

- Event types: Wedding, Corporate, Birthday
- Event location focus: Bengaluru
- Budget planning in Indian Rupees
- Vendor recommendation by category
- 6-week event preparation plan
- Knowledge search for event guidance
- Web dashboard and API-based plan generation
- Markdown and JSON export

### Out of Scope
The initial release will not require:

- Multi-city vendor coverage
- Payment processing
- End-to-end booking transactions
- Guest RSVP management
- Mobile app support
- Real-time vendor marketplace bidding
- Full CRM features

---

## 5. User Personas

### 5.1 Event Planner
The event planner will need fast budget estimates, vendor shortlisting, and presentation-ready reports. The system will help the planner reduce manual research and create a plan that can be shared with clients.

### 5.2 Corporate Coordinator
The corporate coordinator will need structured planning for business events, with emphasis on timelines, cost control, and reliable vendor matching. The system will need to produce professional output quickly and consistently.

### 5.3 Individual User
The individual user will need an easy way to understand what an event will cost and what actions must happen before the event date. The system will need to present guidance in a simple, accessible format.

---

## 6. Core Features

### 6.1 AI Event Planner
The system will accept event details and will generate a complete event plan.

#### Inputs
- Event type
- Guest count
- Budget
- Event month
- Location
- User preferences

#### Outputs
- Event summary
- Budget split
- Timeline
- Task checklist
- Vendor categories required
- Risk notes
- Exportable plan

#### Behavior
- The system must validate input ranges before planning.
- The system must support a guided form as well as structured API input.
- The system must produce the same high-level plan structure for all supported event types.
- The system must adapt content based on event type and guest count.

#### Must Do
- The planner must return a usable plan within a short response time.
- The planner must not require the user to manually assemble each planning component.
- The planner must present a consistent structure so users can compare events.

---

### 6.2 Budget Optimizer
The system will estimate budget allocation across key event categories.

#### Inputs
- Event type
- Guest count
- Total budget
- Event month
- Weekend flag

#### Outputs
- Catering allocation
- Venue allocation
- Decor allocation
- Percentages for each category
- Per-guest cost breakdown

#### Behavior
- The budget engine must convert user-entered budget values into the internal currency unit expected by the model.
- The optimizer must return category-level amounts that sum to the original total budget.
- The optimizer must adjust outputs according to event type-specific spending patterns.
- The optimizer must be deterministic for the same inputs unless model updates are introduced.

#### Must Do
- The optimizer must never return category totals that exceed the provided total budget after normalization.
- The optimizer must make category splits understandable to non-technical users.
- The optimizer must explain the output in both absolute amount and percentage terms.

---

### 6.3 RAG Knowledge Assistant
The system will answer event planning questions using a curated knowledge base.

#### Inputs
- Free-form user query
- Optional top-k retrieval count

#### Outputs
- Retrieved planning guidance
- Vendor advice
- Timeline tips
- Contextual recommendations

#### Behavior
- The assistant must retrieve semantically relevant content from the knowledge base.
- The assistant must prefer Bengaluru-specific advice when available.
- The assistant must return concise and useful guidance instead of raw document dumps.
- The assistant must support both question-answering and vendor search style queries.

#### Must Do
- The knowledge assistant must support queries such as venue selection, timeline design, and planning best practices.
- The assistant must provide results that can be attached to the final event plan.
- The assistant must allow the planner agent to reuse retrieved text as reasoning support.

---

### 6.4 Multi-Agent System
The system will coordinate specialized agents to build a full plan.

#### Agents
- Planner Agent
- Budget Agent
- Knowledge Agent

#### Behavior
- The Planner Agent must assemble the final plan from other tool outputs.
- The Budget Agent must compute cost allocation and normalize values.
- The Knowledge Agent must retrieve relevant guidance and vendor references.
- The orchestration layer must manage agent sequencing and fallbacks.

#### Must Do
- The agent system must support a demo mode when no LLM key is available.
- The agent system must still complete planning workflows even when the model provider is unavailable.
- The agent system must return structured results that the dashboard can render without manual transformation.

---

### 6.5 Dashboard UI
The system will expose an interactive dashboard for planning.

#### Required UI Elements
- Event type selector
- Guest count slider
- Budget slider
- Month selector
- Location input
- Generate Plan button
- Financial summary cards
- Pie chart visualization
- Timeline sections
- Vendor cards
- Risk section
- Export controls

#### Behavior
- The dashboard must clearly separate input, analysis, and output sections.
- The dashboard must update based on the user’s chosen event details.
- The dashboard must present results in a readable and professional layout.
- The dashboard must support downloads from the same screen where results are shown.

#### Must Do
- The UI must make the planning result easy to scan.
- The UI must not force the user to inspect raw JSON to understand the plan.
- The UI must support both desktop and responsive viewing.

---

### 6.6 Vendor Recommendations
The system will recommend vendors by category.

#### Vendor Categories
- Catering
- Venue
- Decor

#### Behavior
- The system must match vendor recommendations to the event type and budget profile.
- The system must show estimated cost per vendor.
- The system must assign a visible rating or relevance score.
- The system must surface a short descriptive note for each vendor.

#### Must Do
- Vendor recommendations must be explained in the context of the plan.
- The system must not recommend irrelevant vendors without justification.
- The recommendations must be usable by a planner for next-step outreach.

---

### 6.7 Export and Sharing
The system will support export of generated plans.

#### Export Formats
- Markdown
- JSON

#### Behavior
- The system must allow users to download a human-readable version of the plan.
- The system must allow users to download a machine-readable version of the plan.
- The system must preserve the plan structure in both formats.

#### Must Do
- The exported Markdown must be professional and presentation-ready.
- The exported JSON must be structured for integration or automation.

---

## 7. Functional Requirements

### FR1: Event Input Capture
The system will accept event type, budget, guest count, location, and month.

- The system must validate values before processing.
- The system must reject unsupported event types.
- The system must support both beginner-friendly UI input and API input.

### FR2: Budget Prediction
The system will compute budget allocation using the ML budget engine.

- The system must use the correct feature order and encoding expected by the model.
- The system must normalize predicted values to the user budget.
- The system must return both percentage and currency outputs.

### FR3: Knowledge Retrieval
The system will retrieve relevant event guidance from the knowledge base.

- The system must support semantic search queries.
- The system must return top matching knowledge snippets.
- The system must present retrieved guidance in plain language.

### FR4: Vendor Matching
The system will recommend vendors for the required categories.

- The system must match vendor category to event plan category.
- The system must show estimated cost and rating.
- The system must keep vendor recommendations aligned with budget splits.

### FR5: Event Timeline Generation
The system will produce a 6-week planning timeline.

- The system must break the plan into week-by-week actions.
- The system must include operational, vendor, and coordination tasks.
- The system must adjust the timeline depending on event type and scale.

### FR6: Plan Export
The system will enable export of the final event plan.

- The system must support Markdown and JSON export.
- The system must keep exports consistent with dashboard output.
- The system must name exports in a predictable format.

### FR7: Risk Mitigation
The system will identify common event risks.

- The system must include a contingency budget recommendation.
- The system must mention likely planning risks such as weather, traffic, and vendor changes.
- The system must propose mitigation strategies in the plan.

### FR8: Agent Orchestration
The system will coordinate multiple agents or tools to complete planning.

- The system must route work to the correct agent.
- The system must provide a fallback when live LLM access is not available.
- The system must preserve structured output across the workflow.

---

## 8. Workflow Requirements

### Workflow 1: Quick Budget Estimation
1. The user will enter event details.
2. The system will validate the request.
3. The budget engine will calculate category splits.
4. The dashboard will display financial summary cards and a pie chart.
5. The user will review per-guest cost and contingency guidance.

### Workflow 2: Full Event Plan Generation
1. The user will submit event type, budget, guest count, month, and location.
2. The system will compute budget splits.
3. The system will retrieve relevant knowledge base content.
4. The agent layer will assemble a complete plan.
5. The dashboard will present timeline, vendors, risks, and export options.

### Workflow 3: Knowledge Query
1. The user will ask a planning question.
2. The system will embed the query.
3. The retrieval layer will fetch relevant passages.
4. The assistant will return a concise answer with useful guidance.

### Workflow 4: Vendor Review
1. The planner will review vendor recommendations.
2. The system will show matching vendors by category.
3. The planner will compare cost and rating.
4. The planner will use the export to share the list externally.

### Workflow 5: Download and Share
1. The user will choose Markdown or JSON.
2. The system will build the export payload.
3. The file will be downloaded with the generated event plan.
4. The user will share or archive the result.

---

## 9. Behavior Requirements

The product will behave as follows:

- It will respond to the same event inputs with consistent plan structure.
- It will adapt outputs based on event type and budget.
- It will explain financial output in simple business terms.
- It will return useful guidance rather than raw technical artifacts.
- It will continue operating in limited mode if the LLM provider is unavailable.
- It will expose a stable API contract for the dashboard and any future clients.

---

## 10. Data and Model Requirements

### ML Data
- The system will train on Bengaluru-style synthetic event data.
- The model will expect a fixed feature schema.
- The model pipeline must preserve feature order, scaling, and encoding.

### Knowledge Base Data
- The knowledge base will include event guides, planning tips, and vendor references.
- The data will be indexed for semantic retrieval.
- The knowledge base must support incremental expansion later.

### Output Data
- Generated plans will contain summary, financial, timeline, vendor, and risk sections.
- Exported JSON must remain schema-consistent.
- Exported Markdown must remain readable outside the application.

---

## 11. Non-Functional Requirements

### Performance
- Budget prediction should complete quickly enough for interactive use.
- Full plan generation should complete within a user-friendly wait time.
- Dashboard pages should load without noticeable delay.

### Reliability
- The system must continue functioning when the LLM provider is offline.
- The API must return structured error responses.
- The dashboard must show clear failure states when services are unavailable.

### Usability
- The product must be understandable by non-technical users.
- The layout must make the planning flow obvious.
- Labels, metrics, and outputs must use plain business language.

### Maintainability
- The codebase must remain modular by phase.
- The orchestration logic must remain separable from UI rendering.
- The system must support future city expansion without redesigning the entire platform.

### Security
- User input must be validated before use.
- The system must avoid leaking internal errors in user-facing views.
- Optional API key configuration must be isolated in environment settings.

---

## 12. Success Criteria

The product will be considered successful when it can:

- Accept event details from a user without confusion
- Produce a complete budget split and timeline
- Return relevant vendor guidance from the knowledge base
- Generate a professional event plan end to end
- Export plans in Markdown and JSON
- Operate with or without live LLM access
- Support Bengaluru planning use cases reliably

---

## 13. Future Releases

Future versions may add:

- Multi-city vendor coverage
- Booking and payment workflows
- Vendor portals
- Guest RSVP workflows
- Analytics and historical planning reports
- Mobile applications
- Advanced negotiation agents

---

## 14. Appendix: Example User Story

**As a** user planning a wedding in Bengaluru,  
**I want** to enter my event type, guest count, and budget,  
**so that** the system will generate a complete plan with a budget split, timeline, vendor suggestions, and downloadable output.

---

**Document Owner:** Product Team  
**Status:** Draft Requirements for Future Implementation  
**Next Review:** After scope approval
