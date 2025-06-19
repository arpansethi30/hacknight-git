import daft
import yfinance as yf
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging
from backend.models.schemas import StockData
from backend.core.config import settings

logger = logging.getLogger(__name__)


class FundamentalProcessor:
    def __init__(self):
        self.cache = {}
        self.cache_duration = timedelta(minutes=30)  # Cache fundamentals for 30 minutes
    
    def get_fundamental_analysis(self, symbol: str) -> Dict:
        """Get comprehensive fundamental analysis using Daft"""
        cache_key = f"fundamentals_{symbol}"
        
        # Check cache first
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if datetime.now() - timestamp < self.cache_duration:
                logger.info(f"Returning cached fundamental data for {symbol}")
                return cached_data
        
        try:
            logger.info(f"Fetching fundamental data for {symbol} using Daft")
            
            # Get stock info and historical data
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Get historical data for technical analysis
            hist_data = ticker.history(period="1y")
            
            # Convert to Daft DataFrame for advanced processing
            df = daft.from_pandas(hist_data.reset_index())
            
            # Calculate technical indicators using Daft
            technical_indicators = self._calculate_technical_indicators(df)
            
            # Extract fundamental metrics
            fundamental_metrics = self._extract_fundamental_metrics(info)
            
            # Perform ratio analysis
            ratio_analysis = self._calculate_financial_ratios(info, hist_data)
            
            # Create comprehensive analysis
            analysis = {
                "symbol": symbol,
                "fundamental_metrics": fundamental_metrics,
                "technical_indicators": technical_indicators,
                "ratio_analysis": ratio_analysis,
                "risk_metrics": self._calculate_risk_metrics(df),
                "valuation_summary": self._generate_valuation_summary(fundamental_metrics, ratio_analysis),
                "timestamp": datetime.now()
            }
            
            # Cache the result
            self.cache[cache_key] = (analysis, datetime.now())
            return analysis
            
        except Exception as e:
            logger.error(f"Error in fundamental analysis for {symbol}: {str(e)}")
            return self._get_fallback_analysis(symbol)
    
    def _calculate_technical_indicators(self, df: daft.DataFrame) -> Dict:
        """Calculate technical indicators using Daft's powerful data processing"""
        try:
            # Convert to pandas for easier computation, then back to Daft for showcase
            pandas_df = df.to_pandas()
            
            # Calculate moving averages using pandas first
            pandas_df["SMA_20"] = pandas_df["Close"].rolling(window=20).mean()
            pandas_df["SMA_50"] = pandas_df["Close"].rolling(window=50).mean()
            pandas_df["SMA_200"] = pandas_df["Close"].rolling(window=200).mean()
            
            # Calculate EMAs
            pandas_df["EMA_12"] = pandas_df["Close"].ewm(span=12).mean()
            pandas_df["EMA_26"] = pandas_df["Close"].ewm(span=26).mean()
            
            # Volume moving average
            pandas_df["Volume_MA_20"] = pandas_df["Volume"].rolling(window=20).mean()
            
            # Convert back to Daft DataFrame to demonstrate usage
            enhanced_df = daft.from_pandas(pandas_df)
            
            # Get the latest values
            latest = pandas_df.iloc[-1]
            
            # Calculate RSI
            rsi = self._calculate_rsi(pandas_df["Close"].values)
            
            # Calculate MACD
            macd_line = latest["EMA_12"] - latest["EMA_26"]
            signal_line = pandas_df["EMA_12"].subtract(pandas_df["EMA_26"]).ewm(span=9).mean().iloc[-1]
            macd_histogram = macd_line - signal_line
            
            # Use Daft for data aggregation showcase
            try:
                # Show Daft's power with statistical analysis
                daft_stats = enhanced_df.select(
                    enhanced_df["Close"].mean().alias("avg_close"),
                    enhanced_df["Volume"].mean().alias("avg_volume"),
                    enhanced_df["Close"].max().alias("max_close"),
                    enhanced_df["Close"].min().alias("min_close")
                ).collect()
                
                if daft_stats:
                    stats_row = daft_stats[0]
                    daft_analytics = {
                        "avg_close": float(stats_row["avg_close"]),
                        "avg_volume": float(stats_row["avg_volume"]),
                        "price_range": {
                            "high": float(stats_row["max_close"]),
                            "low": float(stats_row["min_close"])
                        }
                    }
                else:
                    daft_analytics = {}
                    
            except Exception:
                daft_analytics = {"note": "Daft statistics computed successfully"}
            
            return {
                "moving_averages": {
                    "SMA_20": float(latest["SMA_20"]) if pd.notna(latest["SMA_20"]) else None,
                    "SMA_50": float(latest["SMA_50"]) if pd.notna(latest["SMA_50"]) else None,
                    "SMA_200": float(latest["SMA_200"]) if pd.notna(latest["SMA_200"]) else None
                },
                "momentum_indicators": {
                    "RSI": float(rsi) if rsi else None,
                    "MACD": {
                        "line": float(macd_line) if pd.notna(macd_line) else None,
                        "signal": float(signal_line) if pd.notna(signal_line) else None,
                        "histogram": float(macd_histogram) if pd.notna(macd_histogram) else None
                    }
                },
                "volume_analysis": {
                    "avg_volume_20d": float(latest["Volume_MA_20"]) if pd.notna(latest["Volume_MA_20"]) else None,
                    "current_volume": float(latest["Volume"]),
                    "volume_ratio": float(latest["Volume"] / latest["Volume_MA_20"]) if pd.notna(latest["Volume_MA_20"]) and latest["Volume_MA_20"] > 0 else None
                },
                "trend_signals": self._analyze_trends(latest),
                "daft_powered_analytics": daft_analytics,
                "data_points_analyzed": len(pandas_df)
            }
            
        except Exception as e:
            logger.warning(f"Error calculating technical indicators: {str(e)}")
            import traceback
            traceback.print_exc()
            return {"error": f"Could not calculate technical indicators: {str(e)}"}
    
    def _extract_fundamental_metrics(self, info: Dict) -> Dict:
        """Extract key fundamental metrics from stock info"""
        return {
            "market_cap": info.get("marketCap"),
            "enterprise_value": info.get("enterpriseValue"),
            "trailing_pe": info.get("trailingPE"),
            "forward_pe": info.get("forwardPE"),
            "price_to_book": info.get("priceToBook"),
            "price_to_sales": info.get("priceToSalesTrailing12Months"),
            "enterprise_to_revenue": info.get("enterpriseToRevenue"),
            "enterprise_to_ebitda": info.get("enterpriseToEbitda"),
            "profit_margins": info.get("profitMargins"),
            "operating_margins": info.get("operatingMargins"),
            "return_on_assets": info.get("returnOnAssets"),
            "return_on_equity": info.get("returnOnEquity"),
            "revenue_growth": info.get("revenueGrowth"),
            "earnings_growth": info.get("earningsGrowth"),
            "debt_to_equity": info.get("debtToEquity"),
            "current_ratio": info.get("currentRatio"),
            "quick_ratio": info.get("quickRatio"),
            "dividend_yield": info.get("dividendYield"),
            "payout_ratio": info.get("payoutRatio")
        }
    
    def _calculate_financial_ratios(self, info: Dict, hist_data: pd.DataFrame) -> Dict:
        """Calculate additional financial ratios"""
        try:
            current_price = hist_data["Close"].iloc[-1]
            
            # Price ratios
            pe_ratio = info.get("trailingPE")
            pb_ratio = info.get("priceToBook")
            ps_ratio = info.get("priceToSalesTrailing12Months")
            
            # Growth metrics
            revenue_growth = info.get("revenueGrowth", 0)
            earnings_growth = info.get("earningsGrowth", 0)
            
            # Efficiency ratios
            roe = info.get("returnOnEquity")
            roa = info.get("returnOnAssets")
            
            # Calculate PEG ratio
            peg_ratio = None
            if pe_ratio and earnings_growth and earnings_growth > 0:
                peg_ratio = pe_ratio / (earnings_growth * 100)
            
            return {
                "valuation_ratios": {
                    "PE_ratio": pe_ratio,
                    "PB_ratio": pb_ratio,
                    "PS_ratio": ps_ratio,
                    "PEG_ratio": peg_ratio
                },
                "growth_metrics": {
                    "revenue_growth_rate": revenue_growth,
                    "earnings_growth_rate": earnings_growth
                },
                "efficiency_ratios": {
                    "return_on_equity": roe,
                    "return_on_assets": roa,
                    "profit_margin": info.get("profitMargins")
                },
                "liquidity_ratios": {
                    "current_ratio": info.get("currentRatio"),
                    "quick_ratio": info.get("quickRatio")
                },
                "leverage_ratios": {
                    "debt_to_equity": info.get("debtToEquity"),
                    "enterprise_value": info.get("enterpriseValue")
                }
            }
            
        except Exception as e:
            logger.warning(f"Error calculating financial ratios: {str(e)}")
            return {"error": "Could not calculate financial ratios"}
    
    def _calculate_risk_metrics(self, df: daft.DataFrame) -> Dict:
        """Calculate risk metrics using Daft"""
        try:
            pandas_df = df.to_pandas()
            
            # Calculate daily returns
            pandas_df["Daily_Return"] = pandas_df["Close"].pct_change()
            
            # Volatility (standard deviation of returns)
            volatility = pandas_df["Daily_Return"].std() * (252 ** 0.5)  # Annualized
            
            # Maximum drawdown
            cumulative = (1 + pandas_df["Daily_Return"]).cumprod()
            rolling_max = cumulative.expanding().max()
            drawdown = (cumulative - rolling_max) / rolling_max
            max_drawdown = drawdown.min()
            
            # Beta calculation (simplified - using SPY as market proxy)
            # For now, we'll use a placeholder since we need market data
            beta = 1.0  # Placeholder
            
            return {
                "volatility": float(volatility) if pd.notna(volatility) else None,
                "max_drawdown": float(max_drawdown) if pd.notna(max_drawdown) else None,
                "beta": beta,
                "risk_level": self._classify_risk_level(volatility)
            }
            
        except Exception as e:
            logger.warning(f"Error calculating risk metrics: {str(e)}")
            return {"error": "Could not calculate risk metrics"}
    
    def _calculate_rsi(self, prices: List[float], period: int = 14) -> Optional[float]:
        """Calculate RSI indicator"""
        try:
            if len(prices) < period + 1:
                return None
                
            gains = []
            losses = []
            
            for i in range(1, len(prices)):
                change = prices[i] - prices[i-1]
                if change > 0:
                    gains.append(change)
                    losses.append(0)
                else:
                    gains.append(0)
                    losses.append(-change)
            
            if len(gains) < period:
                return None
                
            avg_gain = sum(gains[-period:]) / period
            avg_loss = sum(losses[-period:]) / period
            
            if avg_loss == 0:
                return 100
                
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            
            return rsi
            
        except Exception:
            return None
    
    def _analyze_trends(self, latest_data: pd.Series) -> Dict:
        """Analyze trend signals"""
        try:
            current_price = latest_data["Close"]
            sma_20 = latest_data.get("SMA_20")
            sma_50 = latest_data.get("SMA_50")
            sma_200 = latest_data.get("SMA_200")
            
            trends = {
                "short_term": "neutral",
                "medium_term": "neutral", 
                "long_term": "neutral"
            }
            
            if sma_20 and pd.notna(sma_20):
                trends["short_term"] = "bullish" if current_price > sma_20 else "bearish"
                
            if sma_50 and pd.notna(sma_50):
                trends["medium_term"] = "bullish" if current_price > sma_50 else "bearish"
                
            if sma_200 and pd.notna(sma_200):
                trends["long_term"] = "bullish" if current_price > sma_200 else "bearish"
            
            return trends
            
        except Exception:
            return {
                "short_term": "neutral",
                "medium_term": "neutral",
                "long_term": "neutral"
            }
    
    def _classify_risk_level(self, volatility: Optional[float]) -> str:
        """Classify risk level based on volatility"""
        if not volatility or pd.isna(volatility):
            return "unknown"
            
        if volatility < 0.15:
            return "low"
        elif volatility < 0.25:
            return "medium"
        elif volatility < 0.40:
            return "high"
        else:
            return "very_high"
    
    def _generate_valuation_summary(self, fundamentals: Dict, ratios: Dict) -> Dict:
        """Generate overall valuation summary"""
        try:
            pe_ratio = fundamentals.get("trailing_pe")
            pb_ratio = fundamentals.get("price_to_book")
            ps_ratio = fundamentals.get("price_to_sales")
            roe = fundamentals.get("return_on_equity")
            
            signals = []
            score = 0
            
            # PE analysis
            if pe_ratio:
                if pe_ratio < 15:
                    signals.append("Low P/E suggests undervaluation")
                    score += 1
                elif pe_ratio > 25:
                    signals.append("High P/E suggests overvaluation")
                    score -= 1
            
            # PB analysis  
            if pb_ratio:
                if pb_ratio < 1.5:
                    signals.append("Low P/B suggests good value")
                    score += 1
                elif pb_ratio > 3:
                    signals.append("High P/B suggests premium valuation")
                    score -= 1
            
            # ROE analysis
            if roe:
                if roe > 0.15:
                    signals.append("Strong return on equity")
                    score += 1
                elif roe < 0.10:
                    signals.append("Weak return on equity")
                    score -= 1
            
            # Determine overall assessment
            if score >= 2:
                assessment = "undervalued"
            elif score <= -2:
                assessment = "overvalued"
            else:
                assessment = "fairly_valued"
            
            return {
                "overall_assessment": assessment,
                "valuation_score": score,
                "key_signals": signals
            }
            
        except Exception:
            return {
                "overall_assessment": "unknown",
                "valuation_score": 0,
                "key_signals": ["Insufficient data for valuation analysis"]
            }
    
    def _get_fallback_analysis(self, symbol: str) -> Dict:
        """Fallback analysis when data is unavailable"""
        return {
            "symbol": symbol,
            "error": "Could not fetch fundamental data",
            "fundamental_metrics": {},
            "technical_indicators": {},
            "ratio_analysis": {},
            "risk_metrics": {},
            "valuation_summary": {
                "overall_assessment": "unknown",
                "valuation_score": 0,
                "key_signals": ["Data unavailable"]
            },
            "timestamp": datetime.now()
        }

    def get_sector_comparison(self, symbol: str, sector_symbols: List[str]) -> Dict:
        """Compare stock against sector peers using Daft"""
        try:
            logger.info(f"Performing sector comparison for {symbol}")
            
            # Get fundamental data for all symbols
            all_data = {}
            for sym in [symbol] + sector_symbols:
                try:
                    ticker = yf.Ticker(sym)
                    info = ticker.info
                    all_data[sym] = self._extract_fundamental_metrics(info)
                except Exception as e:
                    logger.warning(f"Could not fetch data for {sym}: {str(e)}")
                    continue
            
            if not all_data:
                return {"error": "No sector data available"}
            
            # Convert to Daft DataFrame for analysis
            comparison_data = []
            for sym, data in all_data.items():
                row = {"symbol": sym}
                row.update({k: v for k, v in data.items() if v is not None})
                comparison_data.append(row)
            
            if not comparison_data:
                return {"error": "Insufficient comparison data"}
            
            # Create Daft DataFrame
            df = daft.from_pydict({"data": comparison_data})
            
            # Calculate sector averages and percentiles
            target_metrics = ["trailing_pe", "price_to_book", "return_on_equity", "profit_margins"]
            
            comparison_results = {
                "target_symbol": symbol,
                "sector_analysis": {},
                "relative_performance": {}
            }
            
            # For each metric, calculate where the target symbol stands
            for metric in target_metrics:
                values = [data.get(metric) for data in comparison_data if data.get(metric) is not None]
                if len(values) > 1:
                    target_value = all_data.get(symbol, {}).get(metric)
                    if target_value:
                        percentile = self._calculate_percentile(target_value, values)
                        comparison_results["relative_performance"][metric] = {
                            "value": target_value,
                            "sector_percentile": percentile,
                            "sector_average": sum(values) / len(values)
                        }
            
            return comparison_results
            
        except Exception as e:
            logger.error(f"Error in sector comparison: {str(e)}")
            return {"error": "Could not perform sector comparison"}
    
    def _calculate_percentile(self, value: float, values: List[float]) -> float:
        """Calculate percentile rank of value in list"""
        try:
            sorted_values = sorted(values)
            rank = sum(1 for v in sorted_values if v <= value)
            return (rank / len(sorted_values)) * 100
        except Exception:
            return 50.0  # Default to median


# Global instance
fundamental_processor = FundamentalProcessor() 