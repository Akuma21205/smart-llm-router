import React, { useState } from 'react';
import { Search, ShieldAlert, ChevronDown, ChevronUp } from 'lucide-react';
import type { TelemetryItem } from '../types';

interface TelemetryTableProps {
  requests: TelemetryItem[];
  loading: boolean;
}

export const TelemetryTable: React.FC<TelemetryTableProps> = ({ requests, loading }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedRouteFilter, setSelectedRouteFilter] = useState<string>('ALL');
  const [expandedId, setExpandedId] = useState<string | null>(null);

  // Filter requests
  const filteredRequests = requests.filter((item) => {
    const matchesSearch =
      searchTerm === '' ||
      item.query.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.category.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.model.toLowerCase().includes(searchTerm.toLowerCase());

    const matchesRoute =
      selectedRouteFilter === 'ALL' ||
      item.route.toUpperCase() === selectedRouteFilter.toUpperCase();

    return matchesSearch && matchesRoute;
  });

  const toggleExpand = (id: string) => {
    setExpandedId(expandedId === id ? null : id);
  };

  const getRouteBadgeClass = (route: string) => {
    const r = route?.toUpperCase();
    if (r === 'FAST') return 'badge-route-fast';
    if (r === 'CODING') return 'badge-route-coding';
    if (r === 'REASONING') return 'badge-route-reasoning';
    return 'badge-route-default';
  };

  const formatTime = (ts: string) => {
    if (!ts) return '';
    const parts = ts.split(' ');
    return parts.length > 1 ? parts[1] : ts;
  };

  return (
    <div className="telemetry-table-card glass-panel" id="telemetry-log-table">
      <div className="table-header-bar">
        <div className="table-title-wrap">
          <h2 className="table-title">Recent Request Telemetry</h2>
          <span className="table-count-badge">
            {filteredRequests.length} of {requests.length} requests
          </span>
        </div>

        <div className="table-controls">
          {/* Route Filter Pills */}
          <div className="route-filters">
            {['ALL', 'FAST', 'CODING', 'REASONING'].map((route) => (
              <button
                key={route}
                onClick={() => setSelectedRouteFilter(route)}
                className={`route-filter-btn ${selectedRouteFilter === route ? 'active' : ''}`}
              >
                {route}
              </button>
            ))}
          </div>

          {/* Search Box */}
          <div className="table-search-box">
            <Search size={14} className="search-icon" />
            <input
              type="text"
              placeholder="Filter by query, model, category..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="search-input"
            />
          </div>
        </div>
      </div>

      <div className="table-container">
        <table className="telemetry-table">
          <thead>
            <tr>
              <th style={{ width: '90px' }}>Time</th>
              <th>Query Prompt</th>
              <th style={{ width: '110px' }}>Category</th>
              <th style={{ width: '100px' }}>Route</th>
              <th style={{ width: '150px' }}>Target Model</th>
              <th style={{ width: '130px' }}>Confidence</th>
              <th style={{ width: '150px' }}>Latencies (Route / Gen)</th>
              <th style={{ width: '80px' }}>Tokens</th>
              <th style={{ width: '40px' }}></th>
            </tr>
          </thead>
          <tbody>
            {filteredRequests.length === 0 ? (
              <tr>
                <td colSpan={9} className="empty-table-cell">
                  {loading ? 'Loading requests...' : 'No telemetry requests match your filter.'}
                </td>
              </tr>
            ) : (
              filteredRequests.map((item) => {
                const isExpanded = expandedId === item.request_id;
                const isFallback = Boolean(item.fallback_triggered);
                const confPercent = Math.round(item.confidence * 100);

                return (
                  <React.Fragment key={item.request_id}>
                    <tr
                      className={`telemetry-row ${isExpanded ? 'row-expanded' : ''}`}
                      onClick={() => toggleExpand(item.request_id)}
                    >
                      <td className="font-mono text-muted text-sm">{formatTime(item.timestamp)}</td>
                      <td className="query-cell">
                        <div className="query-text" title={item.query}>
                          {item.query}
                        </div>
                      </td>
                      <td>
                        <span className="category-pill">{item.category}</span>
                      </td>
                      <td>
                        <span className={`route-pill ${getRouteBadgeClass(item.route)}`}>
                          {item.route.toUpperCase()}
                        </span>
                      </td>
                      <td>
                        <span className="model-pill font-mono" title={item.model}>
                          {item.model.split('/').pop() || item.model}
                        </span>
                      </td>
                      <td>
                        <div className="table-confidence-wrap">
                          <span className="font-mono text-sm">{confPercent}%</span>
                          <div className="mini-conf-track">
                            <div
                              className={`mini-conf-bar ${
                                item.confidence >= 0.7 ? 'fill-green' : 'fill-amber'
                              }`}
                              style={{ width: `${Math.min(confPercent, 100)}%` }}
                            />
                          </div>
                          {isFallback && (
                            <span title="Fallback Triggered">
                              <ShieldAlert size={14} className="icon-fallback-alert" />
                            </span>
                          )}
                        </div>
                      </td>
                      <td className="font-mono text-sm">
                        <span className="text-emerald">{item.routing_latency_ms.toFixed(0)}ms</span>
                        <span className="text-muted"> / </span>
                        <span className="text-indigo">
                          {item.generation_latency_ms
                            ? item.generation_latency_ms > 1000
                              ? `${(item.generation_latency_ms / 1000).toFixed(1)}s`
                              : `${item.generation_latency_ms.toFixed(0)}ms`
                            : '-'}
                        </span>
                      </td>
                      <td className="font-mono text-sm text-secondary">
                        {(item.input_tokens || 0) + (item.output_tokens || 0)}
                      </td>
                      <td className="expand-cell">
                        {isExpanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                      </td>
                    </tr>

                    {/* Expanded Detail Row */}
                    {isExpanded && (
                      <tr className="detail-row">
                        <td colSpan={9}>
                          <div className="detail-panel">
                            <div className="detail-section">
                              <span className="detail-label">Full Query:</span>
                              <p className="detail-query">{item.query}</p>
                            </div>
                            <div className="detail-meta-grid">
                              <div>
                                <span className="detail-label">Request ID:</span>
                                <span className="font-mono text-sm text-secondary">
                                  {item.request_id}
                                </span>
                              </div>
                              <div>
                                <span className="detail-label">Complexity:</span>
                                <span className="text-sm">{item.complexity.toUpperCase()}</span>
                              </div>
                              <div>
                                <span className="detail-label">Full Model URI:</span>
                                <span className="font-mono text-sm text-secondary">{item.model}</span>
                              </div>
                              <div>
                                <span className="detail-label">Token Breakdown:</span>
                                <span className="font-mono text-sm text-secondary">
                                  Input: {item.input_tokens || 0} | Output: {item.output_tokens || 0}
                                </span>
                              </div>
                              {item.fallback_reason && (
                                <div className="detail-col-full">
                                  <span className="detail-label text-amber">Fallback Reason:</span>
                                  <span className="text-sm text-amber font-mono">
                                    {item.fallback_reason}
                                  </span>
                                </div>
                              )}
                            </div>
                          </div>
                        </td>
                      </tr>
                    )}
                  </React.Fragment>
                );
              })
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
