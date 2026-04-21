"""Market data fetcher using CCXT (Bitget)."""

import ccxt
import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime


class MarketDataFetcher:
    """Fetches market data from Bitget using CCXT."""
    
    def __init__(self):
        self.exchange = ccxt.bitget({
            'enableRateLimit': True,
        })
        
        self.timeframe_map = {
            '1m': '1m',
            '5m': '5m', 
            '15m': '15m',
            '1h': '1h',
            '4h': '4h',
            '1d': '1d',
        }
        
    def get_symbols(self) -> List[Dict[str, str]]:
        """Get available trading symbols."""
        return [
            {'symbol': 'BTCUSDT', 'baseAsset': 'BTC', 'quoteAsset': 'USDT', 'name': 'Bitcoin'},
            {'symbol': 'ETHUSDT', 'baseAsset': 'ETH', 'quoteAsset': 'USDT', 'name': 'Ethereum'},
            {'symbol': 'SOLUSDT', 'baseAsset': 'SOL', 'quoteAsset': 'USDT', 'name': 'Solana'},
            {'symbol': 'BNBUSDT', 'baseAsset': 'BNB', 'quoteAsset': 'USDT', 'name': 'BNB'},
            {'symbol': 'ADAUSDT', 'baseAsset': 'ADA', 'quoteAsset': 'USDT', 'name': 'Cardano'},
        ]
    
    def fetch_candles(
        self, 
        symbol: str = 'BTCUSDT', 
        timeframe: str = '1d', 
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Fetch OHLCV candlestick data.
        
        Args:
            symbol: Trading pair (e.g., 'BTCUSDT')
            timeframe: Timeframe ('1m', '5m', '15m', '1h', '4h', '1d')
            limit: Number of candles to fetch
            
        Returns:
            List of candle dictionaries
        """
        try:
            # Map symbol format for CCXT
            symbol_ccxt = f"{symbol[:-4]}/{symbol[-4:]}"  # BTCUSDT -> BTC/USDT
            
            ohlcv = self.exchange.fetch_ohlcv(
                symbol_ccxt,
                timeframe=self.timeframe_map.get(timeframe, '1d'),
                limit=limit
            )
            
            candles = []
            for row in ohlcv:
                candles.append({
                    'time': datetime.fromtimestamp(row[0] / 1000).strftime('%Y-%m-%d'),
                    'open': float(row[1]),
                    'high': float(row[2]),
                    'low': float(row[3]),
                    'close': float(row[4]),
                    'volume': float(row[5]),
                    'change': float(((row[4] - row[1]) / row[1]) * 100),
                })
                
            return candles
            
        except Exception as e:
            print(f"Error fetching candles: {e}")
            return []
    
    def get_summary(self, symbol: str = 'BTCUSDT') -> Dict[str, Any]:
        """Get trading summary for a symbol."""
        candles = self.fetch_candles(symbol, '1d', 90)
        
        if not candles:
            return {}
            
        last = candles[-1]
        prev = candles[-2] if len(candles) > 1 else last
        
        price_change = last['close'] - prev['close']
        price_change_pct = (price_change / prev['close']) * 100 if prev['close'] != 0 else 0
        
        return {
            'symbol': symbol,
            'currentPrice': last['close'],
            'priceChange24h': price_change,
            'priceChangePct24h': price_change_pct,
            'volume24h': last['volume'],
        }