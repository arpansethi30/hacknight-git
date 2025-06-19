import asyncio
from typing import List, Dict, Optional
from datetime import datetime
import logging
from friendli.friendli import AsyncFriendli
from backend.models.schemas import NewsArticle, SentimentAnalysis
from backend.core.config import settings

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    def __init__(self):
        self.client = None
        self.model_name = "llama-3.1-8b-instruct"  # Fast, efficient model
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize FriendliAI client"""
        try:
            if settings.friendli_api_key and settings.friendli_api_key != "your_friendli_api_key_here":
                self.client = AsyncFriendli(token=settings.friendli_api_key)
                logger.info("FriendliAI client initialized successfully")
            else:
                logger.warning("FriendliAI API key not provided, using fallback sentiment analysis")
                self.client = None
        except Exception as e:
            logger.error(f"Failed to initialize FriendliAI client: {str(e)}")
            self.client = None
    
    async def analyze_news_sentiment(self, news_articles: List[NewsArticle]) -> List[NewsArticle]:
        """Analyze sentiment for a list of news articles"""
        if not news_articles:
            return []
        
        analyzed_articles = []
        
        # Process articles with rate limiting to avoid API issues
        for i, article in enumerate(news_articles):
            try:
                logger.info(f"Analyzing article {i+1}/{len(news_articles)}: {article.title[:50]}...")
                sentiment_score = await self._analyze_single_article(article)
                article.sentiment_score = sentiment_score
                analyzed_articles.append(article)
                
                # Add small delay between API calls to avoid rate limiting
                if i < len(news_articles) - 1:  # Don't delay after last item
                    await asyncio.sleep(0.1)  # 100ms delay
                    
            except Exception as e:
                logger.warning(f"Failed to analyze sentiment for article '{article.title[:30]}...': {str(e)}")
                # Use fallback sentiment analysis
                article.sentiment_score = self._fallback_sentiment(article)
                analyzed_articles.append(article)
        
        return analyzed_articles
    
    async def _analyze_single_article(self, article: NewsArticle) -> float:
        """Analyze sentiment of a single article"""
        if not self.client:
            logger.debug("No FriendliAI client, using fallback sentiment")
            return self._fallback_sentiment(article)
        
        # Prepare the text for analysis
        text_to_analyze = f"{article.title}. {article.description or ''}"[:500]  # Limit length
        
        prompt = f"""Analyze the financial sentiment of this news article about a stock/company.

Article: "{text_to_analyze}"

Rate the sentiment on a scale from -1.0 to 1.0 where:
- -1.0 = Very negative (likely to hurt stock price)
- -0.5 = Negative (bearish sentiment)
- 0.0 = Neutral (no clear impact)
- 0.5 = Positive (bullish sentiment)  
- 1.0 = Very positive (likely to boost stock price)

Consider factors like:
- Financial performance mentions
- Market outlook
- Company strategy
- Regulatory news
- Economic indicators

Respond with only the numerical sentiment score (e.g., 0.7, -0.3, 0.0):"""

        try:
            response = await self._call_friendli_api(prompt)
            sentiment_score = self._parse_sentiment_response(response)
            logger.debug(f"FriendliAI sentiment for '{article.title[:30]}...': {sentiment_score}")
            return sentiment_score
        except Exception as e:
            logger.warning(f"FriendliAI API call failed for '{article.title[:30]}...': {str(e)}")
            fallback_score = self._fallback_sentiment(article)
            logger.debug(f"Using fallback sentiment: {fallback_score}")
            return fallback_score
    
    async def _call_friendli_api(self, prompt: str) -> str:
        """Call FriendliAI API with correct serverless endpoint"""
        try:
            response = await self.client.serverless.chat.complete(
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="meta-llama-3.1-8b-instruct",  # Use exact model name
                max_tokens=50,
                temperature=0.1  # Low temperature for consistent results
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"FriendliAI API error: {str(e)}")
            raise
    
    def _parse_sentiment_response(self, response: str) -> float:
        """Parse sentiment score from LLM response"""
        try:
            # Extract number from response
            import re
            numbers = re.findall(r'-?\d*\.?\d+', response)
            if numbers:
                score = float(numbers[0])
                # Clamp to valid range
                return max(-1.0, min(1.0, score))
            else:
                logger.warning(f"Could not parse sentiment from response: {response}")
                return 0.0
        except Exception as e:
            logger.warning(f"Error parsing sentiment response: {str(e)}")
            return 0.0
    
    def _fallback_sentiment(self, article: NewsArticle) -> float:
        """Simple keyword-based sentiment analysis as fallback"""
        text = f"{article.title} {article.description or ''}".lower()
        
        # Financial positive keywords
        positive_keywords = [
            'profit', 'growth', 'increase', 'beat', 'exceed', 'strong', 'record',
            'buy', 'bullish', 'upgrade', 'outperform', 'rally', 'surge', 'gains',
            'earnings beat', 'revenue growth', 'positive outlook', 'expansion'
        ]
        
        # Financial negative keywords
        negative_keywords = [
            'loss', 'decline', 'fall', 'drop', 'miss', 'weak', 'concern',
            'sell', 'bearish', 'downgrade', 'underperform', 'crash', 'plunge',
            'earnings miss', 'revenue decline', 'negative outlook', 'layoffs'
        ]
        
        positive_count = sum(1 for keyword in positive_keywords if keyword in text)
        negative_count = sum(1 for keyword in negative_keywords if keyword in text)
        
        if positive_count > negative_count:
            return min(0.8, positive_count * 0.2)
        elif negative_count > positive_count:
            return max(-0.8, -negative_count * 0.2)
        else:
            return 0.0
    
    async def calculate_aggregate_sentiment(self, news_articles: List[NewsArticle], symbol: str) -> SentimentAnalysis:
        """Calculate aggregate sentiment for a stock"""
        if not news_articles:
            return SentimentAnalysis(
                symbol=symbol,
                overall_sentiment=0.0,
                positive_count=0,
                negative_count=0,
                neutral_count=0,
                news_articles=[],
                timestamp=datetime.now()
            )
        
        # Analyze sentiment for all articles
        analyzed_articles = await self.analyze_news_sentiment(news_articles)
        
        # Calculate aggregate metrics
        sentiment_scores = [a.sentiment_score for a in analyzed_articles if a.sentiment_score is not None]
        
        if sentiment_scores:
            overall_sentiment = sum(sentiment_scores) / len(sentiment_scores)
        else:
            overall_sentiment = 0.0
        
        # Count sentiment categories
        positive_count = sum(1 for score in sentiment_scores if score > 0.2)
        negative_count = sum(1 for score in sentiment_scores if score < -0.2)
        neutral_count = len(sentiment_scores) - positive_count - negative_count
        
        return SentimentAnalysis(
            symbol=symbol,
            overall_sentiment=overall_sentiment,
            positive_count=positive_count,
            negative_count=negative_count,
            neutral_count=neutral_count,
            news_articles=analyzed_articles,
            timestamp=datetime.now()
        )


# Global instance
sentiment_analyzer = SentimentAnalyzer() 