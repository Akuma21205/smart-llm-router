import React, { useState } from 'react';
import { Play, Sparkles, AlertCircle, CheckCircle2, CornerDownLeft, Shield } from 'lucide-react';
import { sendChatMessage } from '../api';
import type { ChatResponse } from '../types';

interface LiveTesterProps {
  onQueryComplete: () => void;
}

const PRESETS = [
  {
    label: '⚡ Fast / General',
    query: 'What is the speed of light in vacuum in kilometers per second?',
  },
  {
    label: '💻 Coding Task',
    query: 'Write an asynchronous retry decorator in Python with exponential backoff and jitter.',
  },
  {
    label: '🧠 Complex Reasoning',
    query: 'Analyze the trade-offs between Paxos and Raft consensus algorithms regarding leader election and log compaction.',
  },
  {
    label: '🎭 Masked Ambiguity',
    query: '[MASK] analyze the performance of [REDACTED] system under unknown multi-variable conditions.',
  },
];

export const LiveTester: React.FC<LiveTesterProps> = ({ onQueryComplete }) => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ChatResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleRun = async (queryText?: string) => {
    const textToRun = (queryText !== undefined ? queryText : query).trim();
    if (!textToRun || loading) return;

    setLoading(true);
    setError(null);
    try {
      const response = await sendChatMessage(textToRun);
      setResult(response);
      onQueryComplete();
    } catch (err: any) {
      setError(err.message || 'Routing request failed.');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      handleRun();
    }
  };

  const getRouteClass = (route: string) => {
    const r = route?.toUpperCase();
    if (r === 'FAST') return 'badge-route-fast';
    if (r === 'CODING') return 'badge-route-coding';
    if (r === 'REASONING') return 'badge-route-reasoning';
    return 'badge-route-default';
  };

  return (
    <div className="live-tester-container glass-panel" id="live-query-tester">
      <div className="tester-header">
        <div className="tester-title-wrap">
          <div className="tester-badge-icon">
            <Sparkles size={18} className="icon-sparkle" />
          </div>
          <div>
            <h2 className="tester-title">Interactive Router Sandbox</h2>
            <p className="tester-subtitle">
              Test semantic classification, confidence gating, and model dispatch in real-time
            </p>
          </div>
        </div>

        {/* Quick Presets */}
        <div className="presets-list">
          <span className="presets-label">Presets:</span>
          {PRESETS.map((p, idx) => (
            <button
              key={idx}
              type="button"
              className="preset-pill"
              onClick={() => {
                setQuery(p.query);
                handleRun(p.query);
              }}
              disabled={loading}
            >
              {p.label}
            </button>
          ))}
        </div>
      </div>

      {/* Query Input Box */}
      <div className="query-input-section">
        <div className="textarea-wrapper">
          <textarea
            id="tester-query-input"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type any prompt to test semantic routing (e.g. 'Solve this dynamic programming problem...' or '[MASK] evaluate...') Ctrl+Enter to run"
            rows={3}
            disabled={loading}
            className="query-textarea"
          />
          <div className="input-action-bar">
            <span className="shortcut-hint">
              <CornerDownLeft size={12} /> Press <b>Ctrl + Enter</b> to dispatch
            </span>
            <button
              id="btn-dispatch-query"
              onClick={() => handleRun()}
              disabled={loading || !query.trim()}
              className={`dispatch-button ${loading ? 'dispatching' : ''}`}
            >
              {loading ? (
                <>
                  <span className="button-spinner" />
                  <span>Routing via Jev & NIM...</span>
                </>
              ) : (
                <>
                  <Play size={15} fill="currentColor" />
                  <span>Route & Run</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="tester-error-box">
          <AlertCircle size={18} />
          <span>{error}</span>
        </div>
      )}

      {/* Live Result Cards */}
      {result && (
        <div className="tester-result-panel">
          <div className="result-routing-grid">
            {/* Step 1: Semantic Intent & Confidence */}
            <div className="routing-step-card">
              <span className="step-tag">1. Jev Classification</span>
              <div className="step-content">
                <div className="step-row">
                  <span className="step-label">Category:</span>
                  <span className="step-badge category-badge">
                    {result.routing.category.toUpperCase()}
                  </span>
                </div>
                <div className="step-row">
                  <span className="step-label">Complexity:</span>
                  <span className="step-badge complexity-badge">
                    {result.routing.complexity.toUpperCase()}
                  </span>
                </div>
                <div className="step-row">
                  <span className="step-label">Confidence:</span>
                  <div className="confidence-wrapper">
                    <span className="step-val font-mono">
                      {(result.routing.confidence * 100).toFixed(0)}%
                    </span>
                    <div className="confidence-bar-bg">
                      <div
                        className={`confidence-bar-fill ${
                          result.routing.confidence >= 0.70 ? 'fill-green' : 'fill-amber'
                        }`}
                        style={{ width: `${Math.min(result.routing.confidence * 100, 100)}%` }}
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Step 2: Policy & Model Route */}
            <div className="routing-step-card">
              <span className="step-tag">2. Policy Decision Matrix</span>
              <div className="step-content">
                <div className="step-row">
                  <span className="step-label">Assigned Route:</span>
                  <span className={`step-badge ${getRouteClass(result.routing.route)}`}>
                    {result.routing.route.toUpperCase()}
                  </span>
                </div>
                <div className="step-row">
                  <span className="step-label">Target Model:</span>
                  <span className="step-val font-mono model-name" title={result.routing.model}>
                    {result.routing.model.split('/').pop() || result.routing.model}
                  </span>
                </div>
                <div className="step-row">
                  <span className="step-label">Safeguard Status:</span>
                  {result.routing.fallback_triggered ? (
                    <span className="fallback-pill-active" title={result.routing.fallback_reason || ''}>
                      <Shield size={12} /> Fallback Triggered
                    </span>
                  ) : (
                    <span className="fallback-pill-normal">
                      <CheckCircle2 size={12} /> Primary Provider
                    </span>
                  )}
                </div>
              </div>
            </div>

            {/* Step 3: Latency & Tokens */}
            <div className="routing-step-card">
              <span className="step-tag">3. Performance Telemetry</span>
              <div className="step-content">
                <div className="step-row">
                  <span className="step-label">Routing Latency:</span>
                  <span className="step-val font-mono text-emerald">
                    {result.routing.routing_latency_ms.toFixed(1)} ms
                  </span>
                </div>
                <div className="step-row">
                  <span className="step-label">Generation Latency:</span>
                  <span className="step-val font-mono text-indigo">
                    {(result.routing.generation_latency_ms / 1000).toFixed(2)} s
                  </span>
                </div>
                <div className="step-row">
                  <span className="step-label">Tokens:</span>
                  <span className="step-val font-mono text-secondary">
                    {result.routing.input_tokens} in / {result.routing.output_tokens} out
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Generated Answer Display */}
          <div className="generated-answer-box">
            <div className="answer-header">
              <div className="answer-title-wrap">
                <CheckCircle2 size={16} className="text-emerald" />
                <span className="answer-title">Model Response</span>
              </div>
              <span className="request-id-tag font-mono">ID: {result.request_id}</span>
            </div>
            <div className="answer-body font-mono">
              <pre>{result.answer}</pre>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
