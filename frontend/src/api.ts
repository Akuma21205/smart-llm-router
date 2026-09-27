import type { StatsResponse, TelemetryItem, HealthStatus, ChatResponse } from './types';

export async function fetchStats(): Promise<StatsResponse> {
  const res = await fetch('/stats');
  if (!res.ok) {
    throw new Error(`Failed to fetch stats: ${res.statusText}`);
  }
  return res.json();
}

export async function fetchRecentTelemetry(limit = 50): Promise<TelemetryItem[]> {
  const res = await fetch(`/telemetry/recent?limit=${limit}`);
  if (!res.ok) {
    throw new Error(`Failed to fetch telemetry: ${res.statusText}`);
  }
  return res.json();
}

export async function fetchHealth(): Promise<HealthStatus> {
  const res = await fetch('/health');
  if (!res.ok) {
    throw new Error(`Failed to fetch health status: ${res.statusText}`);
  }
  return res.json();
}

export async function sendChatMessage(query: string): Promise<ChatResponse> {
  const res = await fetch('/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query }),
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(errorData.detail || `Failed to route chat query: ${res.statusText}`);
  }
  return res.json();
}
