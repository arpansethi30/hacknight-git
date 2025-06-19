#!/usr/bin/env python3
import sys
sys.path.append('.')
import asyncio

async def test_friendli_real():
    """Test actual FriendliAI API call"""
    print("🧪 Testing Real FriendliAI API Integration...")
    
    try:
        from backend.llm.sentiment_analyzer import sentiment_analyzer
        
        # Test basic client
        print(f"✅ Client initialized: {sentiment_analyzer.client is not None}")
        
        # Test a simple single article
        from backend.models.schemas import NewsArticle
        from datetime import datetime
        
        test_article = NewsArticle(
            title="Apple reports strong quarterly earnings beat expectations",
            description="Apple Inc. exceeded Wall Street expectations with strong iPhone sales",
            content="Test content",
            url="https://example.com",
            source="Test Source",
            published_at=datetime.now()
        )
        
        print("🔍 Testing sentiment analysis on single article...")
        sentiment_score = await sentiment_analyzer._analyze_single_article(test_article)
        print(f"📊 Sentiment Score: {sentiment_score}")
        
        if sentiment_score != 0.0:  # Not fallback
            print("🎉 SUCCESS: Using real FriendliAI API!")
        else:
            print("⚠️  Using fallback analysis")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_friendli_real()) 