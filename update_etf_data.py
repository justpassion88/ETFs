#!/usr/bin/env python3
"""
Script to update ETF (Exchange Traded Fund) data using vnstock library.
This script fetches ETF data from Vietnamese stock market.
"""

import pandas as pd
from datetime import datetime, timedelta
from vnstock import Listing, Quote, Fund


def get_etf_list(use_sample=False):
    """
    Get list of all ETFs trading on Vietnamese stock exchanges.
    
    Args:
        use_sample (bool): If True, return sample ETF data instead of fetching from API
    
    Returns:
        pandas.DataFrame: List of ETF symbols with information
    """
    # Sample ETF data for testing/demo when API is not available
    sample_etfs = pd.DataFrame([
        {'symbol': 'FUEVFVND', 'organ_name': 'Quỹ ETF DCVFMVN DIAMOND', 'exchange': 'HOSE'},
        {'symbol': 'E1VFVN30', 'organ_name': 'Quỹ ETF SSIAM VN30', 'exchange': 'HOSE'},
        {'symbol': 'FUESSV50', 'organ_name': 'Quỹ ETF SSIAM VNFIN LEAD', 'exchange': 'HOSE'},
        {'symbol': 'FUESSV30', 'organ_name': 'Quỹ ETF SSIAM VNX50', 'exchange': 'HOSE'},
        {'symbol': 'FUEVN100', 'organ_name': 'Quỹ ETF DCVFMVN VN100', 'exchange': 'HOSE'},
        {'symbol': 'FUESSVFL', 'organ_name': 'Quỹ ETF SSIAM VNFIN LEAD', 'exchange': 'HOSE'},
        {'symbol': 'FUEDCMID', 'organ_name': 'Quỹ ETF DCDS MIDCAP', 'exchange': 'HOSE'},
        {'symbol': 'FUEMAV30', 'organ_name': 'Quỹ ETF MAFM VN30', 'exchange': 'HOSE'},
    ])
    
    if use_sample:
        print(f"Using sample data: Found {len(sample_etfs)} ETFs")
        return sample_etfs
    
    try:
        listing = Listing(source="VCI")
        
        # Get all symbols
        all_symbols = listing.all_symbols()
        
        # Filter for ETFs - Vietnamese ETFs typically have 'Quỹ ETF' in organ_name
        if all_symbols is not None and not all_symbols.empty:
            # Check if required columns exist
            if 'symbol' not in all_symbols.columns or 'organ_name' not in all_symbols.columns:
                print("Warning: Missing required columns in data, using sample data")
                return sample_etfs
            
            # Filter ETFs by organ_name containing 'ETF' (more reliable than symbol prefix)
            etf_symbols = all_symbols[
                all_symbols['organ_name'].str.contains('ETF', case=False, na=False)
            ]
            
            print(f"Found {len(etf_symbols)} ETFs")
            return etf_symbols
        else:
            print("No symbols found, using sample data")
            return sample_etfs
            
    except Exception as e:
        print(f"Error getting ETF list: {e}")
        print("Using sample data as fallback")
        return sample_etfs


def get_etf_historical_data(symbol, start_date=None, end_date=None, use_sample=False):
    """
    Get historical price data for a specific ETF.
    
    Args:
        symbol (str): ETF symbol (e.g., 'FUEVFVND', 'E1VFVN30')
        start_date (str): Start date in 'YYYY-MM-DD' format
        end_date (str): End date in 'YYYY-MM-DD' format
        use_sample (bool): If True, return sample data instead of fetching from API
    
    Returns:
        pandas.DataFrame: Historical price data
    """
    if start_date is None:
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    # Generate sample data for demo
    if use_sample:
        print(f"Using sample data for {symbol}")
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        sample_data = pd.DataFrame({
            'time': dates,
            'open': [10000 + i*10 for i in range(len(dates))],
            'high': [10050 + i*10 for i in range(len(dates))],
            'low': [9950 + i*10 for i in range(len(dates))],
            'close': [10020 + i*10 for i in range(len(dates))],
            'volume': [1000000 + i*1000 for i in range(len(dates))]
        })
        print(f"Generated {len(sample_data)} sample records for {symbol}")
        return sample_data
    
    try:
        print(f"Fetching data for {symbol} from {start_date} to {end_date}...")
        
        quote = Quote(source="VCI", symbol=symbol)
        df = quote.history(start=start_date, end=end_date, interval="1D")
        
        if df is not None and not df.empty:
            print(f"Retrieved {len(df)} records for {symbol}")
            return df
        else:
            print(f"No data found for {symbol}")
            return pd.DataFrame()
            
    except Exception as e:
        print(f"Error getting historical data for {symbol}: {e}")
        return pd.DataFrame()


def get_etf_fund_info(symbol, use_sample=False):
    """
    Get fund information for an ETF.
    
    Args:
        symbol (str): ETF symbol
        use_sample (bool): If True, return sample data instead of fetching from API
    
    Returns:
        pandas.DataFrame: Fund information
    """
    # Sample fund info for demo
    if use_sample:
        sample_info = pd.DataFrame([{
            'symbol': symbol,
            'nav': 10500,
            'nav_change': 0.5,
            'trading_date': datetime.now().strftime('%Y-%m-%d')
        }])
        print(f"Using sample fund info for {symbol}")
        return sample_info
    
    try:
        fund = Fund(source="VCI")
        info = fund.nav(symbol=symbol)
        
        if info is not None and not info.empty:
            print(f"Retrieved fund info for {symbol}")
            return info
        else:
            print(f"No fund info found for {symbol}")
            return pd.DataFrame()
            
    except Exception as e:
        print(f"Error getting fund info for {symbol}: {e}")
        return pd.DataFrame()


def save_etf_data_to_excel(etf_list, output_file="etf_data.xlsx", use_sample=False):
    """
    Save ETF data to Excel file with multiple sheets.
    
    Args:
        etf_list (pandas.DataFrame): List of ETF symbols
        output_file (str): Output Excel file name
        use_sample (bool): If True, use sample data instead of fetching from API
    """
    try:
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Save ETF list
            etf_list.to_excel(writer, sheet_name='ETF_List', index=False)
            print(f"Saved ETF list to sheet 'ETF_List'")
            
            # Get data for top 5 ETFs (or all if less than 5)
            top_etfs = etf_list.head(5)
            
            for idx, row in top_etfs.iterrows():
                symbol = row['symbol']
                
                # Get historical data
                historical_data = get_etf_historical_data(symbol, use_sample=use_sample)
                if not historical_data.empty:
                    # Excel sheet name limit is 31 characters
                    sheet_name = f"{symbol}_Price"[:31]
                    historical_data.to_excel(writer, sheet_name=sheet_name, index=False)
                    print(f"Saved price data for {symbol}")
                
                # Get fund info
                fund_info = get_etf_fund_info(symbol, use_sample=use_sample)
                if not fund_info.empty:
                    # Excel sheet name limit is 31 characters
                    sheet_name = f"{symbol}_Info"[:31]
                    fund_info.to_excel(writer, sheet_name=sheet_name, index=False)
                    print(f"Saved fund info for {symbol}")
        
        print(f"\nData successfully saved to {output_file}")
        
    except Exception as e:
        print(f"Error saving data to Excel: {e}")


def main(use_sample=False):
    """
    Main function to update ETF data.
    
    Args:
        use_sample (bool): If True, use sample data instead of fetching from API.
                          Useful for testing or when API is not available.
    """
    print("=" * 60)
    print("ETF Data Update Script using vnstock")
    print("=" * 60)
    
    if use_sample:
        print("⚠️  Running in SAMPLE DATA mode (no API calls)")
    
    print()
    
    # Get list of ETFs
    etf_list = get_etf_list(use_sample=use_sample)
    
    if not etf_list.empty:
        print(f"\nETF Symbols found:")
        print(etf_list[['symbol', 'organ_name']].head(10))
        print()
        
        # Save data to Excel
        save_etf_data_to_excel(etf_list, output_file="etf_data.xlsx", use_sample=use_sample)
    else:
        print("No ETF data found to process")
    
    print("\n" + "=" * 60)
    print("ETF data update completed!")
    print("=" * 60)


if __name__ == "__main__":
    import sys
    
    # Check if --sample flag is provided
    use_sample = "--sample" in sys.argv or "--demo" in sys.argv
    
    if use_sample:
        print("ℹ️  Note: Using sample data for demonstration")
        print("    Remove --sample flag to fetch real data from vnstock API\n")
    
    main(use_sample=use_sample)
