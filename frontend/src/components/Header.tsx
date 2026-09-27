import React from 'react';
import { Activity, RefreshCw, Zap, ShieldCheck } from 'lucide-react';
import type { HealthStatus } from '../types';

interface HeaderProps {
  health: HealthStatus | null;
  loading: boolean;
  lastUpdated: Date | null;
  refreshInterval: number;
  onIntervalChange: (interval: number) => void;
  onRefresh: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  health,
  loading,
  lastUpdated,
  refreshInterval,
  onIntervalChange,
  onRefresh,
}) => {
  return (
    <header className="header-container glass-panel">
      <div className="header-left">
        <div className="header-brand">
          <div className="logo-badge">
            <Zap className="logo-icon" size={22} />
          </div>
          <div>
            <div className="title-row">
              <h1 className="header-title">Smart LLM Router</h1>
              <span className="version-pill">Telemetry & Observability</span>
            </div>
            <p className="header-subtitle">
              Dynamic Semantic Routing with Jev · NVIDIA NIM Primary · OpenRouter Fallback
            </p>
          </div>
        </div>
      </div>

      <div className="header-center">
        <div className="provider-badges">
          <div className="provider-badge">
            <span className="live-pulse-dot" />
            <span className="badge-label">Jev Semantic Layer</span>
          </div>

          <div className={`provider-badge ${health?.primary_provider === 'nvidia' ? 'active' : ''}`}>
            <ShieldCheck size={14} className="badge-icon-nvidia" />
            <span className="badge-label">NVIDIA NIM</span>
          </div>

          <div className={`provider-badge ${health?.fallback_provider === 'openrouter' ? 'active' : ''}`}>
            <Activity size={14} className="badge-icon-openrouter" />
            <span className="badge-label">OpenRouter</span>
          </div>
        </div>
      </div>

      <div className="header-right">
        <div className="auto-refresh-selector">
          <label htmlFor="refresh-select" className="refresh-label">Poll:</label>
          <select
            id="refresh-select"
            value={refreshInterval}
            onChange={(e) => onIntervalChange(Number(e.target.value))}
            className="refresh-select"
          >
            <option value={3000}>3s</option>
            <option value={5000}>5s</option>
            <option value={10000}>10s</option>
            <option value={0}>Manual</option>
          </select>
        </div>

        <button
          id="btn-manual-refresh"
          onClick={onRefresh}
          disabled={loading}
          className={`refresh-button ${loading ? 'loading' : ''}`}
          title="Refresh telemetry and stats"
        >
          <RefreshCw size={15} className={loading ? 'spin-icon' : ''} />
          <span>Refresh</span>
        </button>

        {lastUpdated && (
          <span className="last-sync-time" title={lastUpdated.toISOString()}>
            {lastUpdated.toLocaleTimeString()}
          </span>
        )}
      </div>
    </header>
  );
};
