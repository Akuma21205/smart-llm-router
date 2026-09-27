import React from 'react';
import { Send, Zap, Clock, Cpu, AlertTriangle } from 'lucide-react';
import type { StatsResponse } from '../types';

interface MetricCardsProps {
  stats: StatsResponse | null;
}

export const MetricCards: React.FC<MetricCardsProps> = ({ stats }) => {
  const totalRequests = stats?.total_requests ?? 0;
  const avgRouting = stats?.avg_routing_latency_ms ?? 0;
  const avgGen = stats?.avg_generation_latency_ms ?? 0;
  const inTokens = stats?.total_input_tokens ?? 0;
  const outTokens = stats?.total_output_tokens ?? 0;
  const totalTokens = inTokens + outTokens;
  const fallbacks = stats?.fallback_count ?? 0;
  const fallbackRate = totalRequests > 0 ? ((fallbacks / totalRequests) * 100).toFixed(1) : '0.0';

  const formatNumber = (num: number) => {
    return new Intl.NumberFormat().format(num);
  };

  const formatSeconds = (ms: number) => {
    if (ms >= 1000) {
      return `${(ms / 1000).toFixed(2)}s`;
    }
    return `${ms.toFixed(1)}ms`;
  };

  return (
    <div className="metric-cards-grid">
      {/* Total Requests */}
      <div className="metric-card glass-panel" id="metric-total-requests">
        <div className="metric-header">
          <span className="metric-title">Total Requests</span>
          <div className="metric-icon-wrap icon-cyan">
            <Send size={18} />
          </div>
        </div>
        <div className="metric-value">{formatNumber(totalRequests)}</div>
        <div className="metric-footer">
          <span className="metric-footer-badge badge-cyan">Live SQLite DB</span>
          <span className="metric-subtext">Requests processed</span>
        </div>
      </div>

      {/* Avg Routing Latency */}
      <div className="metric-card glass-panel" id="metric-routing-latency">
        <div className="metric-header">
          <span className="metric-title">Avg Routing Latency</span>
          <div className="metric-icon-wrap icon-emerald">
            <Zap size={18} />
          </div>
        </div>
        <div className="metric-value font-mono">
          {avgRouting.toFixed(1)} <span className="metric-unit">ms</span>
        </div>
        <div className="metric-footer">
          <span className="metric-footer-badge badge-emerald">Jev Classifier</span>
          <span className="metric-subtext">Semantic overhead</span>
        </div>
      </div>

      {/* Avg Generation Latency */}
      <div className="metric-card glass-panel" id="metric-generation-latency">
        <div className="metric-header">
          <span className="metric-title">Avg Generation Latency</span>
          <div className="metric-icon-wrap icon-indigo">
            <Clock size={18} />
          </div>
        </div>
        <div className="metric-value font-mono">
          {formatSeconds(avgGen)}
        </div>
        <div className="metric-footer">
          <span className="metric-footer-badge badge-indigo">NVIDIA NIM / Fallback</span>
          <span className="metric-subtext">Model inference</span>
        </div>
      </div>

      {/* Tokens Processed */}
      <div className="metric-card glass-panel" id="metric-tokens-processed">
        <div className="metric-header">
          <span className="metric-title">Tokens Processed</span>
          <div className="metric-icon-wrap icon-violet">
            <Cpu size={18} />
          </div>
        </div>
        <div className="metric-value font-mono">{formatNumber(totalTokens)}</div>
        <div className="metric-footer">
          <span className="metric-subtext">
            In: <b>{formatNumber(inTokens)}</b> · Out: <b>{formatNumber(outTokens)}</b>
          </span>
        </div>
      </div>

      {/* Fallback Executions */}
      <div className="metric-card glass-panel" id="metric-fallback-count">
        <div className="metric-header">
          <span className="metric-title">Fallbacks & Low Conf</span>
          <div className={`metric-icon-wrap ${fallbacks > 0 ? 'icon-amber' : 'icon-muted'}`}>
            <AlertTriangle size={18} />
          </div>
        </div>
        <div className="metric-value font-mono">
          {fallbacks} <span className="metric-unit">({fallbackRate}%)</span>
        </div>
        <div className="metric-footer">
          <span className={`metric-footer-badge ${fallbacks > 0 ? 'badge-amber' : 'badge-emerald'}`}>
            {fallbacks > 0 ? 'Triggered Safeguard' : 'Nominal'}
          </span>
          <span className="metric-subtext">OpenRouter / Reasoning</span>
        </div>
      </div>
    </div>
  );
};
