#!/usr/bin/env python3
"""Test script for Alpha Vantage market data integration"""

import os
import sys
# Add the project root to the path (go up one directory from tests/)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from src.news_collector import SmartNewsCollector

def test_market_data():
    """Test fetching market data from Alpha Vantage"""
    
    # Load environment variables
    load_dotenv()
    
    # Check if API key is set
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    if not api_key:
        print("=" * 60)
        print("ALPHA VANTAGE API KEY NOT FOUND")
        print("=" * 60)
        print("\nTo get your free API key:")
        print("1. Go to: https://www.alphavantage.co/support/#api-key")
        print("2. Enter your email to get a free API key")
        print("3. Add to your .env file:")
        print("   ALPHA_VANTAGE_API_KEY=your-key-here")
        print("=" * 60)
        return
    
    print("=" * 60)
    print("TESTING ALPHA VANTAGE MARKET DATA")
    print("=" * 60)
    print(f"\nAPI Key found: {api_key[:8]}...")
    
    # Initialize collector and fetch market data
    collector = SmartNewsCollector()
    print("\nFetching market data...\n")
    
    market_data = collector.get_market_data()
    
    if market_data:
        print("\n" + "=" * 60)
        print("MARKET DATA SUCCESSFULLY RETRIEVED")
        print("=" * 60)
        print(f"WTI Crude: ${market_data['wti_crude']:.2f} ({market_data['change_wti']})")
        print(f"Brent Crude: ${market_data['brent_crude']:.2f} ({market_data['change_brent']})")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("FAILED TO RETRIEVE MARKET DATA")
        print("=" * 60)
        print("Check the console output above for error details")

if __name__ == "__main__":
    test_market_data()