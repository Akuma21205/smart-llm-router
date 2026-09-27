import React from 'react';
import ReactECharts from 'echarts-for-react';
import * as echarts from 'echarts';
import { PieChart as PieIcon, BarChart2, TrendingUp } from 'lucide-react';
import type { StatsResponse, TelemetryItem } from '../types';

interface ChartsSectionProps {
  stats: StatsResponse | null;
  recentRequests: TelemetryItem[];
}

export const ChartsSection: React.FC<ChartsSectionProps> = ({ stats, recentRequests }) => {
  // 1. Route Distribution Donut Chart Options
  const routeDist = stats?.route_distribution || {};
  const routeData = Object.entries(routeDist).map(([key, value]) => {
    const upperKey = key.toUpperCase();
    let color = '#06b6d4';
    if (upperKey === 'FAST') color = '#10b981';
    if (upperKey === 'REASONING') color = '#8b5cf6';
    if (upperKey === 'CODING') color = '#06b6d4';

    return {
      name: upperKey,
      value: value,
      itemStyle: { color },
    };
  });

  const routeChartOption = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(15, 23, 42, 0.95)',
      borderColor: 'rgba(255, 255, 255, 0.15)',
      textStyle: { color: '#f8fafc', fontFamily: 'Plus Jakarta Sans, sans-serif' },
      formatter: '{b}: <b>{c}</b> queries ({d}%)',
    },
    legend: {
      bottom: '2%',
      left: 'center',
      textStyle: { color: '#94a3b8', fontSize: 12 },
      itemWidth: 10,
      itemHeight: 10,
    },
    series: [
      {
        name: 'Route Distribution',
        type: 'pie',
        radius: ['52%', '76%'],
        center: ['50%', '45%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 8,
          borderColor: '#0e1422',
          borderWidth: 3,
        },
        label: {
          show: false,
          position: 'center',
        },
        emphasis: {
          scale: true,
          scaleSize: 8,
          label: {
            show: true,
            fontSize: 16,
            fontWeight: '600',
            color: '#f8fafc',
            formatter: '{b}\n{d}%',
          },
        },
        labelLine: { show: false },
        data: routeData.length > 0 ? routeData : [{ name: 'No Data', value: 0, itemStyle: { color: '#334155' } }],
      },
    ],
  };

  // 2. Category / Intent Breakdown Bar Chart Options
  const categoryDist = stats?.category_distribution || {};
  // If category_distribution is empty, derive from recentRequests
  const effectiveCategoryDist =
    Object.keys(categoryDist).length > 0
      ? categoryDist
      : recentRequests.reduce((acc, curr) => {
          acc[curr.category] = (acc[curr.category] || 0) + 1;
          return acc;
        }, {} as Record<string, number>);

  const categoryNames = Object.keys(effectiveCategoryDist);
  const categoryValues = Object.values(effectiveCategoryDist);

  const categoryChartOption = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: 'rgba(15, 23, 42, 0.95)',
      borderColor: 'rgba(255, 255, 255, 0.15)',
      textStyle: { color: '#f8fafc' },
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '8%',
      top: '12%',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      data: categoryNames.map((n) => n.toUpperCase()),
      axisLine: { lineStyle: { color: 'rgba(255, 255, 255, 0.1)' } },
      axisLabel: { color: '#94a3b8', fontSize: 11 },
      axisTick: { show: false },
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      axisLabel: { color: '#64748b' },
      splitLine: { lineStyle: { color: 'rgba(255, 255, 255, 0.05)', type: 'dashed' } },
    },
    series: [
      {
        name: 'Queries',
        type: 'bar',
        barWidth: '38%',
        itemStyle: {
          borderRadius: [6, 6, 0, 0],
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#38bdf8' },
            { offset: 1, color: '#6366f1' },
          ]),
        },
        data: categoryValues,
      },
    ],
  };

  // 3. Performance & Latency Trend (Routing vs Generation)
  const chronologicalRequests = [...recentRequests].reverse().slice(-20);
  const labels = chronologicalRequests.map((r, i) => {
    const timeStr = r.timestamp ? r.timestamp.split(' ')[1] || `Q${i + 1}` : `Q${i + 1}`;
    return timeStr;
  });
  const routingLatencies = chronologicalRequests.map((r) => r.routing_latency_ms);
  const generationLatencies = chronologicalRequests.map((r) => r.generation_latency_ms ?? 0);

  const latencyTrendOption = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(15, 23, 42, 0.95)',
      borderColor: 'rgba(255, 255, 255, 0.15)',
      textStyle: { color: '#f8fafc' },
      formatter: (params: any) => {
        if (!Array.isArray(params) || params.length === 0) return '';
        const idx = params[0].dataIndex;
        const item = chronologicalRequests[idx];
        const querySnippet = item?.query ? `"${item.query.slice(0, 45)}..."` : '';
        let html = `<div style="font-weight:600;margin-bottom:4px;">${querySnippet}</div>`;
        html += `<div style="font-size:12px;color:#94a3b8;margin-bottom:6px;">Route: <b style="color:#38bdf8">${item?.route?.toUpperCase()}</b> | Model: ${item?.model}</div>`;
        params.forEach((p) => {
          html += `<div style="display:flex;justify-content:space-between;gap:12px;font-size:12px;">
            <span>${p.marker} ${p.seriesName}</span>
            <span style="font-family:JetBrains Mono;font-weight:600;">${Number(p.value).toFixed(1)} ms</span>
          </div>`;
        });
        return html;
      },
    },
    legend: {
      top: '0%',
      right: '2%',
      textStyle: { color: '#94a3b8', fontSize: 12 },
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '6%',
      top: '16%',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: labels,
      axisLine: { lineStyle: { color: 'rgba(255, 255, 255, 0.1)' } },
      axisLabel: { color: '#64748b', fontSize: 10 },
      axisTick: { show: false },
    },
    yAxis: {
      type: 'value',
      name: 'ms',
      nameTextStyle: { color: '#64748b' },
      axisLine: { show: false },
      axisLabel: { color: '#64748b' },
      splitLine: { lineStyle: { color: 'rgba(255, 255, 255, 0.05)', type: 'dashed' } },
    },
    series: [
      {
        name: 'Routing Latency (Jev)',
        type: 'line',
        smooth: true,
        showSymbol: false,
        lineStyle: { width: 3, color: '#10b981' },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(16, 185, 129, 0.3)' },
            { offset: 1, color: 'rgba(16, 185, 129, 0.0)' },
          ]),
        },
        data: routingLatencies,
      },
      {
        name: 'Generation Latency',
        type: 'line',
        smooth: true,
        showSymbol: false,
        lineStyle: { width: 3, color: '#8b5cf6' },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(139, 92, 246, 0.25)' },
            { offset: 1, color: 'rgba(139, 92, 246, 0.0)' },
          ]),
        },
        data: generationLatencies,
      },
    ],
  };

  return (
    <div className="charts-grid-container">
      {/* Route Distribution Chart */}
      <div className="chart-card glass-panel" id="chart-route-distribution">
        <div className="chart-card-header">
          <div className="chart-title-wrap">
            <PieIcon size={18} className="chart-icon-route" />
            <h2 className="chart-title">Route Distribution</h2>
          </div>
          <span className="chart-subtitle">Fast vs Coding vs Reasoning</span>
        </div>
        <div className="chart-body">
          <ReactECharts option={routeChartOption} style={{ height: '260px', width: '100%' }} />
        </div>
      </div>

      {/* Category Breakdown Chart */}
      <div className="chart-card glass-panel" id="chart-category-breakdown">
        <div className="chart-card-header">
          <div className="chart-title-wrap">
            <BarChart2 size={18} className="chart-icon-category" />
            <h2 className="chart-title">Query Intent Classification</h2>
          </div>
          <span className="chart-subtitle">Jev semantic category volume</span>
        </div>
        <div className="chart-body">
          <ReactECharts option={categoryChartOption} style={{ height: '260px', width: '100%' }} />
        </div>
      </div>

      {/* Latency Comparison Trend Chart */}
      <div className="chart-card glass-panel chart-card-wide" id="chart-latency-trend">
        <div className="chart-card-header">
          <div className="chart-title-wrap">
            <TrendingUp size={18} className="chart-icon-trend" />
            <h2 className="chart-title">Latency Breakdown Timeline</h2>
          </div>
          <span className="chart-subtitle">Sub-second Jev routing vs LLM inference (last 20 requests)</span>
        </div>
        <div className="chart-body">
          <ReactECharts option={latencyTrendOption} style={{ height: '270px', width: '100%' }} />
        </div>
      </div>
    </div>
  );
};
