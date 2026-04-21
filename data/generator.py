"""Generate test data when API is unavailable."""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any


def generate_test_candles(
    symbol: str = 'BTCUSDT', 
    days: int = 90,
    base_price: float = None
) -> List[Dict[str, Any]]:
    """Generate synthetic candlestick data for testing."""
    
    if base_price is None:
        if 'BTC' in symbol:
            base_price = 42000
        elif 'ETH' in symbol:
            base_price = 2500
        elif 'SOL' in symbol:
            base_price = 120
        elif 'BNB' in symbol:
            base_price = 300
        elif 'ADA' in symbol:
            base_price = 0.5
        else:
            base_price = 100
    
    candles = []
    price = base_price
    start_date = datetime.now() - timedelta(days=days)
    
    for i in range(days):
        date = start_date + timedelta(days=i)
        
        volatility = base_price * 0.025
        trend = (i / 15) * volatility * 0.3
        open_price = price
        
        change = (random.random() - 0.47) * volatility + trend
        close_price = open_price + change
        
        high_price = max(open_price, close_price) + random.random() * volatility * 0.5
        low_price = min(open_price, close_price) - random.random() * volatility * 0.5
        
        volume = (random.random() * 5000 + 2000) * (base_price / 100)
        change_pct = ((close_price - open_price) / open_price) * 100
        
        candles.append({
            'time': date.strftime('%Y-%m-%d'),
            'open': round(open_price, 2),
            'high': round(high_price, 2),
            'low': round(low_price, 2),
            'close': round(close_price, 2),
            'volume': round(volume, 2),
            'change': round(change_pct, 2),
        })
        
        price = close_price
    
    return candles


def generate_test_pnl(candles: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate synthetic P&L data based on candles."""
    
    points = []
    cum_pnl = 0
    peak = 0
    equity = 10000
    in_trade = False
    entry_price = 0
    trade_size = 0
    
    for candle in candles:
        daily_pnl = 0
        
        if not in_trade and random.random() > 0.7:
            in_trade = True
            entry_price = candle['close']
            trade_size = equity * 0.1
        elif in_trade and random.random() > 0.6:
            pnl_pct = (candle['close'] - entry_price) / entry_price
            daily_pnl = trade_size * pnl_pct * (1 if random.random() > 0.45 else -1)
            cum_pnl += daily_pnl
            equity += daily_pnl
            in_trade = False
        elif in_trade:
            daily_pnl = 0
        else:
            daily_pnl = (random.random() - 0.48) * equity * 0.005
            cum_pnl += daily_pnl
            equity += daily_pnl
        
        if equity > peak:
            peak = equity
        drawdown = (peak - equity) / peak * 100 if peak > 0 else 0
        
        points.append({
            'time': candle['time'],
            'pnl': round(cum_pnl, 2),
            'dailyPnl': round(daily_pnl, 2),
            'drawdown': round(drawdown, 2),
            'equity': round(equity, 2),
        })
    
    total_pnl = points[-1]['pnl'] if points else 0
    max_drawdown = max(p['drawdown'] for p in points) if points else 0
    
    returns = [p['dailyPnl'] / 10000 for p in points]
    avg_return = sum(returns) / len(returns) if returns else 0
    std_dev = (sum((r - avg_return) ** 2 for r in returns) / len(returns)) ** 0.5 if returns else 0
    sharpe_ratio = (avg_return / std_dev * (252 ** 0.5)) if std_dev > 0 else 0
    
    positive_days = len([p for p in points if p['dailyPnl'] > 0])
    win_rate = (positive_days / len(points) * 100) if points else 0
    
    return {
        'points': points,
        'totalPnl': round(total_pnl, 2),
        'maxDrawdown': round(max_drawdown, 2),
        'sharpeRatio': round(sharpe_ratio, 2),
        'winRate': round(win_rate, 1),
    }


# Alias for compatibility
generate_test_data = generate_test_candles