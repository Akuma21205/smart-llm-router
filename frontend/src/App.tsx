import React, { useState, useEffect, useCallback, useRef } from 'react';
import { Header } from './components/Header';
import { MetricCards } from './components/MetricCards';
import { ChartsSection } from './components/ChartsSection';
import { LiveTester } from './components/LiveTester';
import { TelemetryTable } from './components/TelemetryTable';
import { fetchStats, fetchRecentTelemetry, fetchHealth } from './api';
import type { StatsResponse, TelemetryItem, HealthStatus } from './types';
import './App.css';

export const App: React.FC = () => {
  const [stats, setStats] = useState<StatsResponse | null>(null);
  const [recentRequests, setRecentRequests] = useState<TelemetryItem[]>([]);
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [loading, setLoading] = useState(false);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);
  const [refreshInterval, setRefreshInterval] = useState<number>(5000);

  const timerRef = useRef<number | null>(null);

  const loadData = useCallback(async (isSilent = false) => {
    if (!isSilent) setLoading(true);
    try {
      const [statsData, telemetryData, healthData] = await Promise.all([
        fetchStats().catch(() => null),
        fetchRecentTelemetry(50).catch(() => []),
        fetchHealth().catch(() => null),
      ]);

      if (statsData) setStats(statsData);
      if (telemetryData) setRecentRequests(telemetryData);
      if (healthData) setHealth(healthData);
      setLastUpdated(new Date());
    } catch (err) {
      console.error('Failed to load telemetry data:', err);
    } finally {
      if (!isSilent) setLoading(false);
    }
  }, []);

  // Initial load
  useEffect(() => {
    loadData(false);
  }, [loadData]);

  // Polling interval effect
  useEffect(() => {
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }

    if (refreshInterval > 0) {
      timerRef.current = window.setInterval(() => {
        loadData(true);
      }, refreshInterval);
    }

    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, [refreshInterval, loadData]);

  return (
    <main className="app-layout">
      {/* Top Navigation & Status */}
      <Header
        health={health}
        loading={loading}
        lastUpdated={lastUpdated}
        refreshInterval={refreshInterval}
        onIntervalChange={setRefreshInterval}
        onRefresh={() => loadData(false)}
      />

      {/* Primary KPI Metrics */}
      <MetricCards stats={stats} />

      {/* Apache ECharts Section */}
      <ChartsSection stats={stats} recentRequests={recentRequests} />

      {/* Interactive Sandbox & Prompt Tester */}
      <LiveTester onQueryComplete={() => loadData(true)} />

      {/* Detailed Telemetry Log Table */}
      <TelemetryTable requests={recentRequests} loading={loading} />
    </main>
  );
};

export default App;
