import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from backend.models.schemas import StockData
import logging

logger = logging.getLogger(__name__)


class StockDataProcessor:
    def __init__(self):
        self.cache = {}
        self.cache_duration = timedelta(minutes=5)
    
    def get_stock_data(self, symbol: str) -> Optional[StockData]:
        """Fetch current stock data for a given symbol"""
        try:
            # Check cache first
            cache_key = f"stock_{symbol}"
            if self._is_cached(cache_key):
                return self.cache[cache_key]["data"]
            
            # Fetch from yfinance
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = ticker.history(period="1d")
            
            if hist.empty:
                logger.warning(f"No data found for symbol: {symbol}")
                return None
            
            latest = hist.iloc[-1]
            previous_close = info.get('previousClose', latest['Close'])
            
            stock_data = StockData(
                symbol=symbol.upper(),
                name=info.get('longName', symbol),
                price=float(latest['Close']),
                change=float(latest['Close'] - previous_close),
                change_percent=float((latest['Close'] - previous_close) / previous_close * 100),
                volume=int(latest['Volume']),
                market_cap=info.get('marketCap'),
                timestamp=datetime.now()
            )
            
            # Cache the result
            self._cache_data(cache_key, stock_data)
            return stock_data
            
        except Exception as e:
            logger.error(f"Error fetching stock data for {symbol}: {str(e)}")
            return None
    
    def get_historical_data(self, symbol: str, period: str = "1mo") -> pd.DataFrame:
        """Fetch historical stock data"""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            return hist
        except Exception as e:
            logger.error(f"Error fetching historical data for {symbol}: {str(e)}")
            return pd.DataFrame()
    
    def get_multiple_stocks(self, symbols: List[str]) -> Dict[str, StockData]:
        """Fetch data for multiple stocks"""
        results = {}
        for symbol in symbols:
            data = self.get_stock_data(symbol)
            if data:
                results[symbol] = data
        return results
    
    def _is_cached(self, key: str) -> bool:
        """Check if data is cached and still valid"""
        if key not in self.cache:
            return False
        
        cached_time = self.cache[key]["timestamp"]
        return datetime.now() - cached_time < self.cache_duration
    
    def _cache_data(self, key: str, data: StockData):
        """Cache stock data"""
        self.cache[key] = {
            "data": data,
            "timestamp": datetime.now()
        }
        
        # Simple cache cleanup - keep only last 100 entries
        if len(self.cache) > 100:
            oldest_key = min(self.cache.keys(), 
                           key=lambda k: self.cache[k]["timestamp"])
            del self.cache[oldest_key]


# Global instance
stock_processor = StockDataProcessor() 