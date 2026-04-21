"""Data module for fetching and processing market data."""

from .fetcher import MarketDataFetcher
from .generator import generate_test_data
from .patterns import detect_patterns, Pattern

__all__ = ['MarketDataFetcher', 'generate_test_data', 'detect_patterns', 'Pattern']