#!/usr/bin/env python3
"""
Example script demonstrating various ways to use the ETF data updater.
"""

from update_etf_data import (
    get_etf_list,
    get_etf_historical_data,
    get_etf_fund_info
)
import pandas as pd


def example_1_list_all_etfs():
    """Example 1: Get and display all ETFs."""
    print("\n" + "="*60)
    print("Example 1: List All ETFs")
    print("="*60)
    
    etf_list = get_etf_list()
    
    if not etf_list.empty:
        print(f"\nTotal ETFs found: {len(etf_list)}")
        print("\nFirst 10 ETFs:")
        print(etf_list[['symbol', 'organ_name', 'exchange']].head(10))
    else:
        print("No ETFs found")


def example_2_get_specific_etf_price():
    """Example 2: Get price data for a specific ETF."""
    print("\n" + "="*60)
    print("Example 2: Get Price Data for Specific ETF")
    print("="*60)
    
    # Popular Vietnam ETFs
    etf_symbols = ['FUEVFVND', 'E1VFVN30', 'FUESSV50']
    
    for symbol in etf_symbols:
        print(f"\nFetching data for {symbol}...")
        df = get_etf_historical_data(
            symbol=symbol,
            start_date="2024-01-01",
            end_date="2024-12-31"
        )
        
        if not df.empty:
            print(f"\nLatest 5 trading days for {symbol}:")
            print(df[['time', 'open', 'high', 'low', 'close', 'volume']].tail(5))
            
            # Calculate basic statistics
            avg_volume = df['volume'].mean()
            price_change = ((df['close'].iloc[-1] - df['close'].iloc[0]) / df['close'].iloc[0]) * 100
            
            print(f"\nStatistics for {symbol}:")
            print(f"  Average Daily Volume: {avg_volume:,.0f}")
            print(f"  Price Change (Year): {price_change:.2f}%")


def example_3_compare_etfs():
    """Example 3: Compare multiple ETFs."""
    print("\n" + "="*60)
    print("Example 3: Compare Multiple ETFs")
    print("="*60)
    
    etf_symbols = ['FUEVFVND', 'E1VFVN30']
    comparison_data = []
    
    for symbol in etf_symbols:
        df = get_etf_historical_data(
            symbol=symbol,
            start_date="2024-01-01",
            end_date="2024-12-31"
        )
        
        if not df.empty:
            # Calculate returns
            initial_price = df['close'].iloc[0]
            final_price = df['close'].iloc[-1]
            total_return = ((final_price - initial_price) / initial_price) * 100
            
            # Calculate volatility (standard deviation of daily returns)
            daily_returns = df['close'].pct_change()
            volatility = daily_returns.std() * 100
            
            comparison_data.append({
                'Symbol': symbol,
                'Initial Price': initial_price,
                'Final Price': final_price,
                'Total Return (%)': round(total_return, 2),
                'Volatility (%)': round(volatility, 2)
            })
    
    if comparison_data:
        comparison_df = pd.DataFrame(comparison_data)
        print("\nETF Comparison (2024):")
        print(comparison_df.to_string(index=False))


def example_4_get_fund_info():
    """Example 4: Get fund information."""
    print("\n" + "="*60)
    print("Example 4: Get Fund Information")
    print("="*60)
    
    symbol = "FUEVFVND"
    print(f"\nFetching fund info for {symbol}...")
    
    fund_info = get_etf_fund_info(symbol)
    
    if not fund_info.empty:
        print(f"\nFund information for {symbol}:")
        print(fund_info)
    else:
        print(f"No fund info available for {symbol}")


def example_5_recent_performance():
    """Example 5: Analyze recent performance."""
    print("\n" + "="*60)
    print("Example 5: Recent Performance Analysis")
    print("="*60)
    
    symbol = "FUEVFVND"
    print(f"\nAnalyzing recent performance for {symbol}...")
    
    # Get last 30 days
    from datetime import datetime, timedelta
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    
    df = get_etf_historical_data(symbol, start_date, end_date)
    
    if not df.empty and len(df) > 0:
        print(f"\nRecent performance for {symbol} (Last 30 days):")
        
        # Calculate metrics
        highest = df['high'].max()
        lowest = df['low'].min()
        avg_close = df['close'].mean()
        latest_close = df['close'].iloc[-1]
        
        print(f"  Highest Price: {highest:,.0f} VND")
        print(f"  Lowest Price: {lowest:,.0f} VND")
        print(f"  Average Price: {avg_close:,.0f} VND")
        print(f"  Latest Price: {latest_close:,.0f} VND")
        
        # Show trend
        if len(df) >= 2:
            price_change = latest_close - df['close'].iloc[0]
            price_change_pct = (price_change / df['close'].iloc[0]) * 100
            trend = "📈 UP" if price_change > 0 else "📉 DOWN"
            
            print(f"\n  30-Day Trend: {trend}")
            print(f"  Price Change: {price_change:,.0f} VND ({price_change_pct:+.2f}%)")


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("ETF Data Examples - Using vnstock")
    print("="*60)
    
    try:
        # Run examples
        example_1_list_all_etfs()
        example_2_get_specific_etf_price()
        example_3_compare_etfs()
        example_4_get_fund_info()
        example_5_recent_performance()
        
        print("\n" + "="*60)
        print("All examples completed!")
        print("="*60)
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        print("Note: Make sure you have installed all requirements:")
        print("  pip install -r requirements.txt")


if __name__ == "__main__":
    main()
