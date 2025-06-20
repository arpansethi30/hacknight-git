import requests
from datetime import datetime, timedelta
from typing import List, Optional
from backend.models.schemas import NewsArticle
from backend.core.config import settings
import logging

logger = logging.getLogger(__name__)


class NewsDataProcessor:
    def __init__(self):
        self.base_url = "https://newsapi.org/v2"
        self.api_key = settings.news_api_key or "demo_key"  # Use demo for now
        self.cache = {}
        self.cache_duration = timedelta(minutes=15)
    
    def get_stock_news(self, symbol: str, days: int = 1) -> List[NewsArticle]:
        """Fetch news articles for a specific stock symbol"""
        try:
            # Check cache first
            cache_key = f"news_{symbol}_{days}"
            if self._is_cached(cache_key):
                return self.cache[cache_key]["data"]
            
            # Calculate date range
            to_date = datetime.now()
            from_date = to_date - timedelta(days=days)
            
            # Build search query - broader for better coverage
            company_name = self._get_company_name(symbol)
            query = f'"{symbol}" OR "{company_name}"'
            
            params = {
                "q": query,
                "from": from_date.strftime("%Y-%m-%d"),
                "to": to_date.strftime("%Y-%m-%d"),
                "sortBy": "publishedAt",
                "apiKey": self.api_key,
                "language": "en",
                "pageSize": 20
            }
            
            response = requests.get(f"{self.base_url}/everything", params=params)
            
            if response.status_code == 200:
                data = response.json()
                articles = self._parse_articles(data.get("articles", []), symbol)
                
                # Cache the result
                self._cache_data(cache_key, articles)
                return articles
            else:
                logger.error(f"News API error: {response.status_code} - {response.text}")
                return self._get_mock_news(symbol)  # Fallback to mock data
                
        except Exception as e:
            logger.error(f"Error fetching news for {symbol}: {str(e)}")
            return self._get_mock_news(symbol)  # Fallback to mock data
    
    def get_market_news(self, category: str = "business") -> List[NewsArticle]:
        """Fetch general market news"""
        try:
            params = {
                "category": category,
                "country": "us",
                "apiKey": self.api_key,
                "pageSize": 10
            }
            
            response = requests.get(f"{self.base_url}/top-headlines", params=params)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_articles(data.get("articles", []), "MARKET")
            else:
                return self._get_mock_market_news()
                
        except Exception as e:
            logger.error(f"Error fetching market news: {str(e)}")
            return self._get_mock_market_news()
    
    def _parse_articles(self, articles: List[dict], symbol: str) -> List[NewsArticle]:
        """Parse raw articles into NewsArticle objects"""
        parsed_articles = []
        company_name = self._get_company_name(symbol)
        
        for article in articles:
            try:
                title = article.get("title", "")
                description = article.get("description", "")
                content = article.get("content", "")
                
                # Filter articles to ensure relevance to the stock (temporarily relaxed)
                # if not self._is_stock_relevant(title, description, content, symbol, company_name):
                #     continue
                
                # Parse published date
                published_str = article.get("publishedAt", "")
                published_at = datetime.fromisoformat(published_str.replace("Z", "+00:00"))
                
                news_article = NewsArticle(
                    title=title,
                    description=description,
                    content=content,
                    url=article.get("url", ""),
                    source=article.get("source", {}).get("name", "Unknown"),
                    published_at=published_at,
                    sentiment_score=None  # Will be filled by sentiment analysis
                )
                
                parsed_articles.append(news_article)
                
            except Exception as e:
                logger.warning(f"Error parsing article: {str(e)}")
                continue
        
        return parsed_articles
    
    def _is_stock_relevant(self, title: str, description: str, content: str, symbol: str, company_name: str) -> bool:
        """Check if article is relevant to the stock"""
        # Combine all text for checking
        full_text = f"{title} {description} {content}".lower()
        
        # Check if the stock symbol or company name appears
        symbol_lower = symbol.lower()
        company_lower = company_name.lower()
        
        # Must contain either symbol or company name (be more flexible)
        has_symbol = symbol_lower in full_text
        has_company = any(word in full_text for word in company_lower.split() if len(word) > 2)
        
        # More inclusive financial/business keywords
        financial_keywords = [
            'stock', 'share', 'earnings', 'revenue', 'profit', 'market', 
            'dividend', 'price', 'trading', 'investor', 'financial', 'quarterly',
            'annual', 'guidance', 'outlook', 'analyst', 'rating', 'buy', 'sell',
            'business', 'company', 'corporation', 'inc', 'technology', 'tech',
            'growth', 'performance', 'report', 'results', 'forecast', 'news'
        ]
        
        has_financial_context = any(keyword in full_text for keyword in financial_keywords)
        
        # If it has symbol or company name, it's likely relevant
        # Or if it has financial context and mentions the symbol/company
        return (has_symbol or has_company) or (has_financial_context and (has_symbol or has_company))
    
    def _get_company_name(self, symbol: str) -> str:
        """Get company name for better search results"""
        # Comprehensive mapping for common stocks
        company_names = {
            "AAPL": "Apple Inc",
            "GOOGL": "Google Alphabet",
            "GOOG": "Google Alphabet", 
            "MSFT": "Microsoft Corporation",
            "AMZN": "Amazon.com",
            "TSLA": "Tesla Inc",
            "META": "Meta Platforms Facebook",
            "NVDA": "NVIDIA Corporation",
            "NFLX": "Netflix Inc",
            "AMD": "Advanced Micro Devices",
            "INTC": "Intel Corporation",
            "CRM": "Salesforce",
            "ORCL": "Oracle Corporation",
            "ADBE": "Adobe Inc",
            "BABA": "Alibaba Group",
            "JPM": "JPMorgan Chase",
            "BAC": "Bank of America",
            "WMT": "Walmart Inc",
            "V": "Visa Inc",
            "MA": "Mastercard Inc",
            "UNH": "UnitedHealth Group",
            "HD": "Home Depot",
            "PG": "Procter Gamble",
            "JNJ": "Johnson Johnson",
            "XOM": "ExxonMobil Corporation",
            "CVX": "Chevron Corporation",
            "PFE": "Pfizer Inc",
            "KO": "Coca-Cola Company",
            "PEP": "PepsiCo Inc",
            "COST": "Costco Wholesale",
            "AVGO": "Broadcom Inc",
            "ASML": "ASML Holding"
        }
        return company_names.get(symbol.upper(), symbol)
    
    def _get_mock_news(self, symbol: str) -> List[NewsArticle]:
        """Generate mock news for demo purposes"""
        mock_articles = [
            NewsArticle(
                title=f"{symbol} Reports Strong Q4 Earnings",
                description=f"{symbol} exceeded analyst expectations with robust revenue growth",
                content=f"Financial analysis shows {symbol} demonstrated strong performance...",
                url=f"https://example.com/news/{symbol.lower()}-earnings",
                source="Financial Demo News",
                published_at=datetime.now() - timedelta(hours=2),
                sentiment_score=0.7
            ),
            NewsArticle(
                title=f"Market Analysis: {symbol} Stock Performance",
                description=f"Technical analysis and market outlook for {symbol}",
                content=f"Detailed market analysis of {symbol} shows positive trends...",
                url=f"https://example.com/analysis/{symbol.lower()}",
                source="Market Analysis Demo",
                published_at=datetime.now() - timedelta(hours=6),
                sentiment_score=0.3
            )
        ]
        return mock_articles
    
    def _get_mock_market_news(self) -> List[NewsArticle]:
        """Generate mock market news"""
        return [
            NewsArticle(
                title="Market Outlook: Tech Stocks Show Resilience",
                description="Technology sector demonstrates strong fundamentals",
                content="Market analysis shows continued growth in tech sector...",
                url="https://example.com/market-outlook",
                source="Demo Market News",
                published_at=datetime.now() - timedelta(hours=1),
                sentiment_score=0.5
            )
        ]
    
    def _is_cached(self, key: str) -> bool:
        """Check if data is cached and still valid"""
        if key not in self.cache:
            return False
        
        cached_time = self.cache[key]["timestamp"]
        return datetime.now() - cached_time < self.cache_duration
    
    def _cache_data(self, key: str, data: List[NewsArticle]):
        """Cache news data"""
        self.cache[key] = {
            "data": data,
            "timestamp": datetime.now()
        }


# Global instance
news_processor = NewsDataProcessor() 