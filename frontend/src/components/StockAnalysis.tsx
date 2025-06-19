'use client';

import { useState, useEffect } from 'react';

interface AnalysisData {
  symbol: string;
  sentiment: {
    overall_sentiment: number;
    positive_count: number;
    negative_count: number;
    neutral_count: number;
    confidence: number;
  };
  fundamentals: {
    pe_ratio: number;
    pb_ratio: number;
    roe: number;
    market_cap: number;
    rsi: number;
    volatility: number;
  };
  recommendation: {
    action: string;
    confidence: number;
    reasoning: string[];
  };
}

export default function StockAnalysis({ symbol = "AAPL" }) {
  const [analysisData, setAnalysisData] = useState<AnalysisData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalysis = async () => {
      try {
        // Fetch comprehensive analysis
        const response = await fetch(`http://localhost:8001/api/v1/analysis/complete/${symbol}`);
        const data = await response.json();
        setAnalysisData(data);
      } catch (error) {
        console.error('Error fetching analysis:', error);
        // Mock data for demo
        setAnalysisData({
          symbol: symbol,
          sentiment: {
            overall_sentiment: 0.25,
            positive_count: 12,
            negative_count: 5,
            neutral_count: 8,
            confidence: 0.85
          },
          fundamentals: {
            pe_ratio: 30.48,
            pb_ratio: 43.97,
            roe: 138.02,
            market_cap: 3020000000000,
            rsi: 43.4,
            volatility: 32.25
          },
          recommendation: {
            action: "Buy",
            confidence: 80,
            reasoning: [
              "Strong fundamental metrics with healthy P/E ratio",
              "Positive sentiment trend in recent news",
              "Technical indicators showing oversold condition"
            ]
          }
        });
      } finally {
        setLoading(false);
      }
    };

    fetchAnalysis();
  }, [symbol]);

  if (loading) {
    return (
      <div className="max-w-6xl mx-auto p-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100 animate-pulse">
              <div className="h-6 bg-gray-200 rounded mb-4"></div>
              <div className="h-4 bg-gray-200 rounded mb-2"></div>
              <div className="h-4 bg-gray-200 rounded w-2/3"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (!analysisData) return null;

  const getSentimentColor = (score: number) => {
    if (score > 0.1) return 'text-green-600 bg-green-100';
    if (score < -0.1) return 'text-red-600 bg-red-100';
    return 'text-gray-600 bg-gray-100';
  };

  const getSentimentLabel = (score: number) => {
    if (score > 0.1) return 'Bullish';
    if (score < -0.1) return 'Bearish';
    return 'Neutral';
  };

  return (
    <div className="max-w-6xl mx-auto p-6" id="sentiment">
      {/* Header */}
      <div className="mb-8 text-center">
        <h2 className="text-3xl font-bold text-gray-800 mb-2">
          Complete Analysis: {analysisData.symbol}
        </h2>
        <p className="text-gray-600">
          AI-powered comprehensive market analysis powered by FriendliAI and Daft
        </p>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        {/* Sentiment Analysis */}
        <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100 card-hover">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-800">AI Sentiment</h3>
            <div className="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center">
              <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
          </div>
          
          <div className="mb-4">
            <div className={`inline-flex px-3 py-1 rounded-full text-sm font-medium ${getSentimentColor(analysisData.sentiment.overall_sentiment)}`}>
              {getSentimentLabel(analysisData.sentiment.overall_sentiment)}
            </div>
          </div>

          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Overall Score</span>
              <span className="font-semibold">{analysisData.sentiment.overall_sentiment.toFixed(3)}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Confidence</span>
              <span className="font-semibold">{(analysisData.sentiment.confidence * 100).toFixed(0)}%</span>
            </div>
            <div className="grid grid-cols-3 gap-2 text-xs">
              <div className="text-center">
                <div className="text-green-600 font-semibold">{analysisData.sentiment.positive_count}</div>
                <div className="text-gray-500">Positive</div>
              </div>
              <div className="text-center">
                <div className="text-gray-600 font-semibold">{analysisData.sentiment.neutral_count}</div>
                <div className="text-gray-500">Neutral</div>
              </div>
              <div className="text-center">
                <div className="text-red-600 font-semibold">{analysisData.sentiment.negative_count}</div>
                <div className="text-gray-500">Negative</div>
              </div>
            </div>
          </div>
        </div>

        {/* Fundamental Metrics */}
        <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100 card-hover" id="fundamentals">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-800">Fundamentals</h3>
            <div className="w-8 h-8 bg-purple-500 rounded-lg flex items-center justify-center">
              <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
          </div>

          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">P/E Ratio</span>
              <span className="font-semibold">{analysisData.fundamentals.pe_ratio.toFixed(2)}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">P/B Ratio</span>
              <span className="font-semibold">{analysisData.fundamentals.pb_ratio.toFixed(2)}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">ROE</span>
              <span className="font-semibold">{analysisData.fundamentals.roe.toFixed(1)}%</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Market Cap</span>
              <span className="font-semibold">${(analysisData.fundamentals.market_cap / 1e12).toFixed(2)}T</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">RSI</span>
              <span className={`font-semibold ${analysisData.fundamentals.rsi < 30 ? 'text-green-600' : analysisData.fundamentals.rsi > 70 ? 'text-red-600' : 'text-gray-800'}`}>
                {analysisData.fundamentals.rsi.toFixed(1)}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Volatility</span>
              <span className="font-semibold">{analysisData.fundamentals.volatility.toFixed(1)}%</span>
            </div>
          </div>
        </div>

        {/* Recommendation */}
        <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100 card-hover">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-800">AI Recommendation</h3>
            <div className="w-8 h-8 bg-green-500 rounded-lg flex items-center justify-center">
              <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
          </div>

          <div className="mb-4">
            <div className={`inline-flex px-4 py-2 rounded-full text-lg font-bold ${
              analysisData.recommendation.action === 'Buy' ? 'bg-green-100 text-green-700' :
              analysisData.recommendation.action === 'Sell' ? 'bg-red-100 text-red-700' :
              'bg-yellow-100 text-yellow-700'
            }`}>
              {analysisData.recommendation.action}
            </div>
          </div>

          <div className="mb-4">
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm text-gray-600">Confidence</span>
              <span className="font-semibold">{analysisData.recommendation.confidence}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-green-500 h-2 rounded-full transition-all"
                style={{ width: `${analysisData.recommendation.confidence}%` }}
              ></div>
            </div>
          </div>

          <div>
            <h4 className="text-sm font-semibold text-gray-700 mb-2">Key Factors:</h4>
            <ul className="space-y-1">
              {analysisData.recommendation.reasoning.map((reason, index) => (
                <li key={index} className="text-xs text-gray-600 flex items-start">
                  <div className="w-1.5 h-1.5 bg-blue-500 rounded-full mt-1.5 mr-2 flex-shrink-0"></div>
                  {reason}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      {/* Technical Chart Placeholder */}
      <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-100">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-xl font-semibold text-gray-800">Technical Analysis</h3>
          <div className="flex space-x-2">
            <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm">RSI: {analysisData.fundamentals.rsi.toFixed(1)}</span>
            <span className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm">Vol: {analysisData.fundamentals.volatility.toFixed(1)}%</span>
          </div>
        </div>

        {/* Chart placeholder with gradient */}
        <div className="h-64 bg-gradient-to-br from-blue-50 to-purple-50 rounded-xl flex items-center justify-center border border-gray-100">
          <div className="text-center">
            <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 12l3-3 3 3 4-4" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
              </svg>
            </div>
            <h4 className="text-lg font-semibold text-gray-700 mb-2">Interactive Chart</h4>
            <p className="text-gray-500 text-sm">
              Real-time price action and technical indicators
            </p>
          </div>
        </div>
      </div>
    </div>
  );
} 