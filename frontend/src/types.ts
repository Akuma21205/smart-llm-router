export interface StatsResponse {
  total_requests: number;
  avg_routing_latency_ms: number;
  avg_generation_latency_ms: number;
  total_input_tokens: number;
  total_output_tokens: number;
  fallback_count: number;
  route_distribution: Record<string, number>;
  model_distribution: Record<string, number>;
  category_distribution?: Record<string, number>;
}

export interface TelemetryItem {
  request_id: string;
  timestamp: string;
  query: string;
  category: string;
  complexity: string;
  route: string;
  model: string;
  confidence: number;
  fallback_triggered: number | boolean;
  fallback_reason?: string | null;
  routing_latency_ms: number;
  generation_latency_ms: number | null;
  input_tokens?: number | null;
  output_tokens?: number | null;
}

export interface HealthStatus {
  status: string;
  primary_provider: string;
  fallback_provider: string;
  jev_configured: boolean;
  confidence_threshold: number;
  models: {
    fast: string;
    coding: string;
    reasoning: string;
    openrouter_fallback: string;
  };
}

export interface ChatResponse {
  request_id: string;
  query: string;
  answer: string;
  routing: {
    category: string;
    complexity: string;
    route: string;
    model: string;
    confidence: number;
    fallback_triggered: boolean;
    fallback_reason?: string | null;
    routing_latency_ms: number;
    generation_latency_ms: number;
    input_tokens: number;
    output_tokens: number;
    estimated_cost_usd: number;
  };
}
