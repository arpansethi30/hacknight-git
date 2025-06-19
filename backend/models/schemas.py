from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime


class StockData(BaseModel):
    symbol: str
    name: Optional[str] = None
    price: float
    change: float
    change_percent: float
    volume: int
    market_cap: Optional[float] = None
    timestamp: datetime


class NewsArticle(BaseModel):
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    url: str
    source: str
    published_at: datetime
    sentiment_score: Optional[float] = None


class SentimentAnalysis(BaseModel):
    symbol: str
    overall_sentiment: float  # -1 to 1
    positive_count: int
    negative_count: int
    neutral_count: int
    news_articles: List[NewsArticle]
    timestamp: datetime


class FundamentalMetrics(BaseModel):
    symbol: str
    pe_ratio: Optional[float] = None
    price_to_book: Optional[float] = None
    debt_to_equity: Optional[float] = None
    return_on_equity: Optional[float] = None
    revenue_growth: Optional[float] = None
    profit_margin: Optional[float] = None
    recommendation: Optional[str] = None
    timestamp: datetime


class StockAnalysisRequest(BaseModel):
    symbol: str
    analysis_type: str = "comprehensive"  # sentiment, fundamental, comprehensive


class StockAnalysisResponse(BaseModel):
    symbol: str
    stock_data: StockData
    sentiment_analysis: Optional[SentimentAnalysis] = None
    fundamental_metrics: Optional[FundamentalMetrics] = None
    recommendation: str
    confidence_score: float
    timestamp: datetime 