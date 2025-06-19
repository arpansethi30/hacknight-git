from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any
from backend.models.schemas import (
    StockData, 
    NewsArticle, 
    StockAnalysisRequest, 
    StockAnalysisResponse
)
from backend.data.stock_processor import stock_processor
from backend.data.news_processor import news_processor
from backend.data.fundamental_processor import fundamental_processor
from backend.llm.sentiment_analyzer import sentiment_analyzer
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Create router
router = APIRouter()


@router.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "FinanceGPT API",
        "version": "1.0.0",
        "timestamp": datetime.now(),
        "features": [
            "Stock Data",
            "News Analysis", 
            "Sentiment Analysis",
            "Fundamental Analysis",
            "AI Recommendations"
        ]
    }


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "services": {
            "stock_processor": "running",
            "news_processor": "running"
        }
    }


@router.get("/stock/{symbol}", response_model=StockData)
async def get_stock(symbol: str):
    """Get current stock data for a symbol"""
    try:
        stock_data = stock_processor.get_stock_data(symbol.upper())
        if not stock_data:
            raise HTTPException(
                status_code=404, 
                detail=f"Stock data not found for symbol: {symbol}"
            )
        return stock_data
    except Exception as e:
        logger.error(f"Error getting stock data: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/stocks/multiple")
async def get_multiple_stocks(symbols: str = "AAPL,GOOGL,MSFT,TSLA"):
    """Get data for multiple stocks"""
    try:
        symbol_list = [s.strip().upper() for s in symbols.split(',')]
        stocks_data = []
        
        for symbol in symbol_list:
            try:
                stock_data = stock_processor.get_stock_data(symbol)
                if stock_data:
                    stocks_data.append(stock_data)
            except Exception as e:
                logger.error(f"Error fetching {symbol}: {e}")
                continue
        
        return {"data": stocks_data, "count": len(stocks_data)}
    except Exception as e:
        logger.error(f"Error fetching multiple stocks: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/news/{symbol}", response_model=List[NewsArticle])
async def get_stock_news(
    symbol: str,
    days: int = Query(1, ge=1, le=7, description="Number of days to fetch news")
):
    """Get news articles for a stock symbol"""
    try:
        news_articles = news_processor.get_stock_news(symbol.upper(), days)
        return news_articles
    except Exception as e:
        logger.error(f"Error getting news: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/news/market", response_model=List[NewsArticle])
async def get_market_news(
    category: str = Query("business", description="News category")
):
    """Get general market news"""
    try:
        news_articles = news_processor.get_market_news(category)
        return news_articles
    except Exception as e:
        logger.error(f"Error getting market news: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/analysis/{symbol}")
async def get_basic_analysis(symbol: str):
    """Get basic analysis combining stock data and news"""
    try:
        # Get stock data
        stock_data = stock_processor.get_stock_data(symbol.upper())
        if not stock_data:
            raise HTTPException(
                status_code=404, 
                detail=f"Stock data not found for symbol: {symbol}"
            )
        
        # Get news
        news_articles = news_processor.get_stock_news(symbol.upper(), 1)
        
        # Calculate basic sentiment (simplified for now)
        positive_count = sum(1 for article in news_articles 
                           if article.sentiment_score and article.sentiment_score > 0.3)
        negative_count = sum(1 for article in news_articles 
                           if article.sentiment_score and article.sentiment_score < -0.3)
        neutral_count = len(news_articles) - positive_count - negative_count
        
        overall_sentiment = 0.0
        if news_articles:
            sentiment_scores = [a.sentiment_score for a in news_articles 
                              if a.sentiment_score is not None]
            if sentiment_scores:
                overall_sentiment = sum(sentiment_scores) / len(sentiment_scores)
        
        # Basic recommendation logic
        recommendation = "Hold"
        if stock_data.change_percent > 5:
            recommendation = "Strong Buy"
        elif stock_data.change_percent > 2:
            recommendation = "Buy"
        elif stock_data.change_percent < -5:
            recommendation = "Strong Sell"
        elif stock_data.change_percent < -2:
            recommendation = "Sell"
        
        return {
            "symbol": symbol.upper(),
            "stock_data": stock_data,
            "news_summary": {
                "total_articles": len(news_articles),
                "positive_count": positive_count,
                "negative_count": negative_count,
                "neutral_count": neutral_count,
                "overall_sentiment": overall_sentiment
            },
            "recommendation": recommendation,
            "confidence_score": min(abs(stock_data.change_percent) / 10, 1.0),
            "timestamp": datetime.now()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in basic analysis: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/sentiment/{symbol}")
async def get_sentiment_analysis(
    symbol: str,
    days: int = Query(1, ge=1, le=7, description="Number of days to analyze"),
    limit: int = Query(5, ge=1, le=20, description="Limit number of articles to analyze")
):
    """Get AI-powered sentiment analysis for a stock"""
    try:
        # Get news articles (limit for faster processing)
        news_articles = news_processor.get_stock_news(symbol.upper(), days)[:limit]
        
        if not news_articles:
            return {
                "symbol": symbol.upper(),
                "message": "No news articles found",
                "overall_sentiment": 0.0,
                "analysis_count": 0
            }
        
        logger.info(f"Analyzing sentiment for {len(news_articles)} articles for {symbol}")
        
        # Perform sentiment analysis
        sentiment_analysis = await sentiment_analyzer.calculate_aggregate_sentiment(
            news_articles, symbol.upper()
        )
        
        return sentiment_analysis
        
    except Exception as e:
        logger.error(f"Error in sentiment analysis: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/analysis/comprehensive/{symbol}")
async def get_comprehensive_analysis(symbol: str):
    """Get comprehensive analysis with sentiment + stock data"""
    try:
        # Get stock data
        stock_data = stock_processor.get_stock_data(symbol.upper())
        if not stock_data:
            raise HTTPException(
                status_code=404, 
                detail=f"Stock data not found for symbol: {symbol}"
            )
        
        # Get sentiment analysis (limit to 3 articles for faster processing)
        news_articles = news_processor.get_stock_news(symbol.upper(), 2)[:3]
        logger.info(f"Performing comprehensive analysis on {len(news_articles)} articles for {symbol}")
        sentiment_analysis = await sentiment_analyzer.calculate_aggregate_sentiment(
            news_articles, symbol.upper()
        )
        
        # Calculate enhanced recommendation
        price_momentum = "bullish" if stock_data.change_percent > 0 else "bearish"
        sentiment_signal = "positive" if sentiment_analysis.overall_sentiment > 0.1 else \
                          "negative" if sentiment_analysis.overall_sentiment < -0.1 else "neutral"
        
        # Combine signals for recommendation
        if price_momentum == "bullish" and sentiment_signal == "positive":
            recommendation = "Strong Buy"
            confidence = 0.9
        elif price_momentum == "bearish" and sentiment_signal == "negative":
            recommendation = "Strong Sell"
            confidence = 0.9
        elif price_momentum == "bullish" and sentiment_signal == "neutral":
            recommendation = "Buy"
            confidence = 0.7
        elif price_momentum == "bearish" and sentiment_signal == "neutral":
            recommendation = "Sell"
            confidence = 0.7
        elif sentiment_signal == "positive" and price_momentum == "bearish":
            recommendation = "Hold (Conflicting Signals)"
            confidence = 0.5
        elif sentiment_signal == "negative" and price_momentum == "bullish":
            recommendation = "Hold (Conflicting Signals)" 
            confidence = 0.5
        else:
            recommendation = "Hold"
            confidence = 0.6
        
        return {
            "symbol": symbol.upper(),
            "stock_data": stock_data,
            "sentiment_analysis": sentiment_analysis,
            "signals": {
                "price_momentum": price_momentum,
                "sentiment_signal": sentiment_signal
            },
            "recommendation": recommendation,
            "confidence_score": confidence,
            "analysis_summary": {
                "total_news_articles": len(news_articles),
                "sentiment_score": sentiment_analysis.overall_sentiment,
                "price_change_24h": stock_data.change_percent
            },
            "timestamp": datetime.now()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in comprehensive analysis: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/fundamentals/{symbol}")
async def get_fundamental_analysis(symbol: str):
    """Get comprehensive fundamental analysis using Daft"""
    try:
        logger.info(f"Fetching fundamental analysis for {symbol} using Daft")
        
        analysis = fundamental_processor.get_fundamental_analysis(symbol.upper())
        return analysis
        
    except Exception as e:
        logger.error(f"Error in fundamental analysis: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/analysis/technical/{symbol}")
async def get_technical_analysis(symbol: str):
    """Get technical indicators analysis using Daft"""
    try:
        logger.info(f"Fetching technical analysis for {symbol}")
        
        # Get the fundamental analysis which includes technical indicators
        full_analysis = fundamental_processor.get_fundamental_analysis(symbol.upper())
        
        # Extract just the technical indicators and risk metrics
        technical_data = {
            "symbol": symbol.upper(),
            "technical_indicators": full_analysis.get("technical_indicators", {}),
            "risk_metrics": full_analysis.get("risk_metrics", {}),
            "timestamp": full_analysis.get("timestamp")
        }
        
        return technical_data
        
    except Exception as e:
        logger.error(f"Error in technical analysis: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/comparison/sector/{symbol}")
async def get_sector_comparison(
    symbol: str,
    peers: str = Query(..., description="Comma-separated list of peer symbols for comparison")
):
    """Compare stock against sector peers using Daft"""
    try:
        logger.info(f"Performing sector comparison for {symbol}")
        
        # Parse peer symbols
        peer_symbols = [s.strip().upper() for s in peers.split(",") if s.strip()]
        
        if not peer_symbols:
            raise HTTPException(status_code=400, detail="At least one peer symbol required")
        
        comparison = fundamental_processor.get_sector_comparison(
            symbol.upper(), peer_symbols
        )
        
        return comparison
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in sector comparison: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/analysis/complete/{symbol}")
async def get_complete_analysis(symbol: str):
    """Get complete analysis combining all data sources: stock, news, sentiment, and fundamentals"""
    try:
        logger.info(f"Performing complete analysis for {symbol}")
        
        # Get all data for comprehensive analysis
        stock_data = stock_processor.get_stock_data(symbol.upper())
        fundamental_data = fundamental_processor.get_fundamental_analysis(symbol.upper())
        
        # News and sentiment (limit for speed)
        news_articles = news_processor.get_stock_news(symbol.upper(), 2)[:3]
        sentiment_analysis = await sentiment_analyzer.calculate_aggregate_sentiment(
            news_articles, symbol.upper()
        )
        
        # Combine all signals for enhanced recommendation
        price_signal = "bullish" if stock_data.change_percent > 0 else "bearish"
        sentiment_signal = "positive" if sentiment_analysis.overall_sentiment > 0.1 else \
                          "negative" if sentiment_analysis.overall_sentiment < -0.1 else "neutral"
        
        # Extract key fundamental signals
        fundamental_signals = fundamental_data.get("valuation_summary", {})
        valuation_assessment = fundamental_signals.get("overall_assessment", "unknown")
        
        # Technical trend signals
        technical_indicators = fundamental_data.get("technical_indicators", {})
        trend_signals = technical_indicators.get("trend_signals", {})
        
        # Generate comprehensive recommendation
        recommendation_score = 0
        confidence_factors = []
        
        # Price momentum
        if price_signal == "bullish":
            recommendation_score += 1
            confidence_factors.append("Positive price momentum")
        elif price_signal == "bearish":
            recommendation_score -= 1
            confidence_factors.append("Negative price momentum")
        
        # Sentiment
        if sentiment_signal == "positive":
            recommendation_score += 1
            confidence_factors.append("Positive market sentiment")
        elif sentiment_signal == "negative":
            recommendation_score -= 1
            confidence_factors.append("Negative market sentiment")
        
        # Fundamentals
        if valuation_assessment == "undervalued":
            recommendation_score += 2
            confidence_factors.append("Fundamentally undervalued")
        elif valuation_assessment == "overvalued":
            recommendation_score -= 2
            confidence_factors.append("Fundamentally overvalued")
        
        # Technical trends
        long_term_trend = trend_signals.get("long_term", "neutral")
        if long_term_trend == "bullish":
            recommendation_score += 1
            confidence_factors.append("Strong long-term trend")
        elif long_term_trend == "bearish":
            recommendation_score -= 1
            confidence_factors.append("Weak long-term trend")
        
        # Final recommendation
        if recommendation_score >= 3:
            final_recommendation = "Strong Buy"
            confidence = 0.95
        elif recommendation_score >= 1:
            final_recommendation = "Buy"
            confidence = 0.80
        elif recommendation_score <= -3:
            final_recommendation = "Strong Sell"
            confidence = 0.95
        elif recommendation_score <= -1:
            final_recommendation = "Sell"
            confidence = 0.80
        else:
            final_recommendation = "Hold"
            confidence = 0.60
        
        return {
            "symbol": symbol.upper(),
            "complete_analysis": {
                "stock_data": stock_data,
                "fundamental_analysis": fundamental_data,
                "sentiment_analysis": sentiment_analysis,
                "signals": {
                    "price_signal": price_signal,
                    "sentiment_signal": sentiment_signal,
                    "valuation_assessment": valuation_assessment,
                    "trend_signals": trend_signals
                },
                "recommendation": {
                    "action": final_recommendation,
                    "confidence_score": confidence,
                    "recommendation_score": recommendation_score,
                    "supporting_factors": confidence_factors
                }
            },
            "powered_by": ["yfinance", "NewsAPI", "FriendliAI", "Daft"],
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        logger.error(f"Error in complete analysis: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/demo/portfolio")
async def demo_portfolio():
    """Demo endpoint showing a sample portfolio analysis"""
    demo_symbols = ["AAPL", "GOOGL", "MSFT", "TSLA"]
    
    try:
        portfolio_data = {}
        for symbol in demo_symbols:
            stock_data = stock_processor.get_stock_data(symbol)
            if stock_data:
                portfolio_data[symbol] = {
                    "stock_data": stock_data,
                    "weight": 25.0  # Equal weight portfolio
                }
        
        # Calculate portfolio performance
        total_change = sum(data["stock_data"].change_percent 
                          for data in portfolio_data.values()) / len(portfolio_data)
        
        return {
            "portfolio": portfolio_data,
            "portfolio_performance": {
                "total_change_percent": total_change,
                "status": "Up" if total_change > 0 else "Down"
            },
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        logger.error(f"Error in demo portfolio: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error") 