'use client';

import { useState } from 'react';
import StockAnalysis from '../components/StockAnalysis';

export default function Home() {
  const [symbol, setSymbol] = useState('AAPL');
  const [inputValue, setInputValue] = useState('AAPL');

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim()) {
      setSymbol(inputValue.trim().toUpperCase());
    }
  };

  return (
    <div className="space-y-8">
      {/* Simple Header */}
      <div className="text-center">
        <h2 className="text-2xl font-medium text-gray-900 mb-2">
          AI-Powered Stock Analysis
        </h2>
        <p className="text-gray-600">
          Enter a stock symbol to get comprehensive AI analysis
        </p>
      </div>

      {/* Search Form */}
      <div className="max-w-md mx-auto">
        <form onSubmit={handleSearch} className="flex gap-3">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Enter stock symbol (e.g. AAPL)"
            className="flex-1 px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <button
            type="submit"
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
          >
            Analyze
          </button>
        </form>
      </div>

      {/* Quick Stock Buttons */}
      <div className="flex justify-center gap-2 flex-wrap">
        {['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'NVDA', 'AMZN'].map((ticker) => (
          <button
            key={ticker}
            onClick={() => {
              setSymbol(ticker);
              setInputValue(ticker);
            }}
            className={`px-3 py-1 text-sm rounded-md transition-colors ${
              symbol === ticker
                ? 'bg-blue-100 text-blue-700 border border-blue-200'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            {ticker}
          </button>
        ))}
      </div>

      {/* Analysis Component */}
      <StockAnalysis symbol={symbol} />
    </div>
  );
}
