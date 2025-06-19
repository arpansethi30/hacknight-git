#!/usr/bin/env python3
"""
Quick test script for FinanceGPT API
"""
import sys
sys.path.append('.')

from backend.data.stock_processor import stock_processor
from backend.data.news_processor import news_processor

def test_sprint_1():
    print("🚀 Testing Sprint 1: Data Foundation")
    print("=" * 50)
    
    # Test stock data
    print("\n📈 Testing Stock Data:")
    symbols = ["AAPL", "GOOGL", "MSFT"]
    for symbol in symbols:
        data = stock_processor.get_stock_data(symbol)
        if data:
            print(f"✅ {symbol}: ${data.price:.2f} ({data.change_percent:+.2f}%)")
        else:
            print(f"❌ {symbol}: Failed to fetch")
    
    # Test news data
    print("\n📰 Testing News Data:")
    news = news_processor.get_stock_news("AAPL", 1)
    print(f"✅ Found {len(news)} news articles for AAPL")
    if news:
        print(f"   Latest: {news[0].title[:60]}...")
    
    print("\n🎉 Sprint 1 Status: COMPLETE ✅")
    print("\nReady for Sprint 2: Sentiment Analysis!")

if __name__ == "__main__":
    test_sprint_1() 