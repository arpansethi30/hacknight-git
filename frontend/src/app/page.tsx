'use client';

import { useState, useEffect } from 'react';
import StockAnalysis from '../components/StockAnalysis';

interface StockData {
  symbol: string;
  name: string;
  price: number;
  change: number;
  change_percent: number;
  volume: number;
  market_cap: number;
}

interface NewsArticle {
  title: string;
  description: string;
  source: string;
  sentiment_score?: number;
}

export default function Home() {
  const [stockData, setStockData] = useState<StockData[]>([]);
  const [newsData, setNewsData] = useState<NewsArticle[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch demo data
    const fetchData = async () => {
      try {
        // Fetch multiple stocks
        const stockResponse = await fetch('http://localhost:8001/api/v1/stocks/multiple?symbols=AAPL,GOOGL,MSFT,TSLA');
        const stockResult = await stockResponse.json();
        setStockData(stockResult.data || []);

        // Fetch news
        const newsResponse = await fetch('http://localhost:8001/api/v1/news/AAPL?days=1');
        const newsResult = await newsResponse.json();
        setNewsData(newsResult.slice(0, 3) || []);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      {/* Hero Section */}
      <section className="bg-white py-24">
        <div className="max-w-6xl mx-auto px-4 text-center">
          <h1 className="text-5xl md:text-7xl font-bold mb-8">
            <span className="gradient-text">AI-Powered</span><br />
            <span className="text-gray-900">Financial Analysis</span>
          </h1>
          
          <p className="text-xl text-gray-600 mb-12 max-w-4xl mx-auto">
            Advanced market intelligence combining real-time data, sentiment analysis, 
            and fundamental insights powered by cutting-edge AI technology.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-16">
            <button className="px-8 py-4 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-lg font-semibold text-lg hover:from-blue-600 hover:to-purple-700 transition-colors">
              Try Live Demo
            </button>
            <button className="px-8 py-4 bg-gray-100 text-gray-800 rounded-lg font-semibold text-lg hover:bg-gray-200 transition-colors">
              View Documentation
            </button>
          </div>

          {/* Tech Stack */}
          <div className="flex flex-wrap justify-center gap-4">
            {['FastAPI', 'FriendliAI', 'Daft', 'yfinance', 'NewsAPI', 'Next.js'].map((tech) => (
              <span key={tech} className="px-4 py-2 bg-gray-100 text-gray-700 rounded-full text-sm font-medium">
                {tech}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* Live Market Data Section */}
      <section id="dashboard" className="bg-gray-50 py-24">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Live Market Data
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Real-time stock prices and market insights powered by our AI platform
            </p>
          </div>

          {/* Stock Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
            {loading ? (
              Array.from({ length: 4 }).map((_, i) => (
                <div key={i} className="bg-white rounded-xl p-6 shadow-lg animate-pulse">
                  <div className="h-4 bg-gray-200 rounded mb-3"></div>
                  <div className="h-8 bg-gray-200 rounded mb-2"></div>
                  <div className="h-4 bg-gray-200 rounded w-1/2"></div>
                </div>
              ))
            ) : (
              stockData.map((stock) => (
                <div key={stock.symbol} className="bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-shadow">
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h3 className="font-bold text-gray-900 text-lg">{stock.symbol}</h3>
                      <p className="text-gray-500 text-sm">{stock.name}</p>
                    </div>
                    <div className={`px-3 py-1 rounded-full text-xs font-semibold ${
                      stock.change_percent >= 0 
                        ? 'bg-green-100 text-green-700' 
                        : 'bg-red-100 text-red-700'
                    }`}>
                      {stock.change_percent >= 0 ? '+' : ''}{stock.change_percent.toFixed(2)}%
                    </div>
                  </div>
                  <div className="mb-3">
                    <p className="text-2xl font-bold text-gray-900">${stock.price.toFixed(2)}</p>
                    <p className={`text-sm ${stock.change >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                      {stock.change >= 0 ? '+' : ''}${stock.change.toFixed(2)}
                    </p>
                  </div>
                  <div className="text-xs text-gray-500">
                    Vol: {(stock.volume / 1000000).toFixed(1)}M
                  </div>
                </div>
              ))
            )}
          </div>

          {/* News Section */}
          <div className="bg-white rounded-xl p-8 shadow-lg">
            <div className="flex items-center justify-between mb-8">
              <h3 className="text-2xl font-bold text-gray-900">Latest Market News</h3>
              <span className="px-4 py-2 bg-blue-100 text-blue-700 rounded-full text-sm font-medium">
                AI Sentiment Analysis
              </span>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {loading ? (
                Array.from({ length: 3 }).map((_, i) => (
                  <div key={i} className="animate-pulse">
                    <div className="h-4 bg-gray-200 rounded mb-2"></div>
                    <div className="h-16 bg-gray-200 rounded mb-3"></div>
                    <div className="h-3 bg-gray-200 rounded w-1/2"></div>
                  </div>
                ))
              ) : (
                newsData.map((article, index) => (
                  <div key={index} className="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                    <h4 className="font-semibold text-gray-900 mb-2 line-clamp-2">
                      {article.title}
                    </h4>
                    <p className="text-gray-600 text-sm mb-3 line-clamp-3">
                      {article.description}
                    </p>
                    <div className="flex justify-between items-center">
                      <span className="text-xs text-gray-500">{article.source}</span>
                      {article.sentiment_score !== undefined && (
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                          article.sentiment_score > 0.1 
                            ? 'bg-green-100 text-green-700' 
                            : article.sentiment_score < -0.1 
                            ? 'bg-red-100 text-red-700'
                            : 'bg-gray-100 text-gray-700'
                        }`}>
                          {article.sentiment_score > 0.1 ? 'Positive' : 
                           article.sentiment_score < -0.1 ? 'Negative' : 'Neutral'}
                        </span>
                      )}
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="analysis" className="bg-white py-24">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Comprehensive Analysis Suite
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Everything you need for intelligent financial decision making
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* FriendliAI Sentiment */}
            <div className="bg-gray-50 rounded-xl p-8 text-center">
              <div className="w-16 h-16 bg-blue-500 rounded-xl flex items-center justify-center mx-auto mb-6">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">AI Sentiment Analysis</h3>
              <p className="text-gray-600 mb-6">
                Real-time sentiment analysis powered by FriendliAI's advanced language models
              </p>
              <ul className="text-sm text-gray-600 space-y-2">
                <li>• News sentiment scoring</li>
                <li>• Market mood analysis</li>
                <li>• Confidence indicators</li>
              </ul>
            </div>

            {/* Daft Fundamentals */}
            <div className="bg-gray-50 rounded-xl p-8 text-center">
              <div className="w-16 h-16 bg-purple-500 rounded-xl flex items-center justify-center mx-auto mb-6">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">Fundamental Analysis</h3>
              <p className="text-gray-600 mb-6">
                Deep financial metrics analysis using Daft's powerful data processing engine
              </p>
              <ul className="text-sm text-gray-600 space-y-2">
                <li>• P/E, P/B, ROE ratios</li>
                <li>• Technical indicators</li>
                <li>• Risk assessments</li>
              </ul>
            </div>

            {/* Real-time Data */}
            <div className="bg-gray-50 rounded-xl p-8 text-center">
              <div className="w-16 h-16 bg-green-500 rounded-xl flex items-center justify-center mx-auto mb-6">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">Real-time Data</h3>
              <p className="text-gray-600 mb-6">
                Live market data integration with intelligent caching and processing
              </p>
              <ul className="text-sm text-gray-600 space-y-2">
                <li>• Live stock prices</li>
                <li>• Market news feeds</li>
                <li>• Volume analytics</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-gray-50 py-24">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-8">
            Ready to Transform Your Trading?
          </h2>
          <p className="text-xl text-gray-600 mb-12">
            Join thousands of traders using AI-powered insights for smarter investment decisions
          </p>
          <button className="px-10 py-4 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-lg font-semibold text-lg hover:from-blue-600 hover:to-purple-700 transition-colors">
            Start Free Trial
          </button>
        </div>
      </section>

      {/* Stock Analysis Demo */}
      <section className="bg-white py-24">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Live Analysis Demo
            </h2>
            <p className="text-xl text-gray-600">
              See our AI-powered analysis in action with real market data
            </p>
          </div>
          <StockAnalysis symbol="AAPL" />
        </div>
      </section>
    </div>
  );
}
