"""Pattern detection for candlestick charts."""

import random
from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum


class PatternType(Enum):
    """Types of candlestick patterns."""
    HAMMER = "Hammer"
    SHOOTING_STAR = "Shooting Star"
    DOJI = "Doji"
    BULLISH_ENGULFING = "Bullish Engulfing"
    BEARISH_ENGULFING = "Bearish Engulfing"
    MORNING_STAR = "Morning Star"
    EVENING_STAR = "Evening Star"
    MARUBOZU = "Marubozu"


@dataclass
class Pattern:
    """Represents a detected candlestick pattern."""
    time: str
    pattern: str
    type: str  # 'bullish' or 'bearish'
    description: str
    strength: int
    price_level: float


def detect_patterns(candles: List[Dict[str, Any]]) -> List[Pattern]:
    """
    Detect candlestick patterns in the data.
    
    Args:
        candles: List of candlestick data
        
    Returns:
        List of detected patterns
    """
    if len(candles) < 3:
        return []
    
    patterns = []
    
    for i in range(2, len(candles)):
        c = candles[i]
        prev = candles[i - 1]
        prev2 = candles[i - 2]
        
        body_size = abs(c['close'] - c['open'])
        total_range = c['high'] - c['low']
        upper_wick = c['high'] - max(c['open'], c['close'])
        lower_wick = min(c['open'], c['close']) - c['low']
        is_bullish = c['close'] > c['open']
        is_bearish = c['close'] < c['open']
        
        # Hammer (bullish reversal)
        if lower_wick > body_size * 2 and upper_wick < body_size * 0.5 and is_bullish:
            patterns.append(Pattern(
                time=c['time'],
                pattern="Hammer",
                type="bullish",
                description="Bullish reversal pattern with long lower wick",
                strength=min(90, 60 + random.randint(0, 30)),
                price_level=c['low'],
            ))
        
        # Shooting Star (bearish reversal)
        if upper_wick > body_size * 2 and lower_wick < body_size * 0.5 and is_bearish:
            patterns.append(Pattern(
                time=c['time'],
                pattern="Shooting Star",
                type="bearish",
                description="Bearish reversal with long upper wick",
                strength=min(90, 55 + random.randint(0, 30)),
                price_level=c['high'],
            ))
        
        # Doji (indecision)
        if total_range > 0 and body_size < total_range * 0.1:
            patterns.append(Pattern(
                time=c['time'],
                pattern="Doji",
                type="bullish" if random.random() > 0.5 else "bearish",
                description="Indecision candle — market at turning point",
                strength=min(75, 45 + random.randint(0, 30)),
                price_level=(c['high'] + c['low']) / 2,
            ))
        
        # Bullish Engulfing
        if (prev['close'] < prev['open'] and 
            c['close'] > c['open'] and 
            c['open'] < prev['close'] and 
            c['close'] > prev['open']):
            patterns.append(Pattern(
                time=c['time'],
                pattern="Bullish Engulfing",
                type="bullish",
                description="Strong bullish reversal — buyers take full control",
                strength=min(95, 70 + random.randint(0, 25)),
                price_level=c['open'],
            ))
        
        # Bearish Engulfing
        if (prev['close'] > prev['open'] and 
            c['close'] < c['open'] and 
            c['open'] > prev['close'] and 
            c['close'] < prev['open']):
            patterns.append(Pattern(
                time=c['time'],
                pattern="Bearish Engulfing",
                type="bearish",
                description="Strong bearish reversal — sellers dominate",
                strength=min(95, 70 + random.randint(0, 25)),
                price_level=c['open'],
            ))
        
        # Morning Star (3-candle bullish)
        if (prev2['close'] < prev2['open'] and 
            abs(prev['close'] - prev['open']) < (prev['high'] - prev['low']) * 0.2 and 
            c['close'] > c['open'] and 
            c['close'] > (prev2['open'] + prev2['close']) / 2):
            patterns.append(Pattern(
                time=c['time'],
                pattern="Morning Star",
                type="bullish",
                description="Three-candle bullish reversal pattern",
                strength=min(95, 80 + random.randint(0, 15)),
                price_level=c['low'],
            ))
        
        # Evening Star (3-candle bearish)
        if (prev2['close'] > prev2['open'] and 
            abs(prev['close'] - prev['open']) < (prev['high'] - prev['low']) * 0.2 and 
            c['close'] < c['open'] and 
            c['close'] < (prev2['open'] + prev2['close']) / 2):
            patterns.append(Pattern(
                time=c['time'],
                pattern="Evening Star",
                type="bearish",
                description="Three-candle bearish reversal pattern",
                strength=min(95, 80 + random.randint(0, 15)),
                price_level=c['high'],
            ))
        
        # Marubozu (strong momentum)
        if (body_size > total_range * 0.7 and 
            is_bullish and 
            upper_wick < body_size * 0.1 and 
            lower_wick < body_size * 0.1):
            patterns.append(Pattern(
                time=c['time'],
                pattern="Marubozu",
                type="bullish",
                description="Full-bodied bullish candle — strong momentum",
                strength=min(90, 65 + random.randint(0, 25)),
                price_level=(c['open'] + c['close']) / 2,
            ))
    
    # Return top 20 patterns sorted by strength
    return sorted(patterns, key=lambda p: p.strength, reverse=True)[:20]


def pattern_to_dict(pattern: Pattern) -> Dict[str, Any]:
    """Convert Pattern to dictionary."""
    return {
        'time': pattern.time,
        'pattern': pattern.pattern,
        'type': pattern.type,
        'description': pattern.description,
        'strength': pattern.strength,
        'priceLevel': pattern.price_level,
    }