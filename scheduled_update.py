#!/usr/bin/env python3
"""
Scheduled ETF data updater with organized folder structure.
Automatically downloads ETF data and saves to date-organized folders.
"""

import os
import pandas as pd
from datetime import datetime
from pathlib import Path
from update_etf_data import (
    get_etf_list,
    get_etf_historical_data,
    get_etf_fund_info
)


def create_output_folder():
    """
    Create output folder structure: ETF/{day}/{month}/{year}
    
    Returns:
        str: Path to the created folder
    """
    now = datetime.now()
    day = now.strftime('%d')
    month = now.strftime('%m')
    year = now.strftime('%Y')
    
    # Create folder structure: ETF/day/month/year
    output_path = os.path.join('ETF', day, month, year)
    Path(output_path).mkdir(parents=True, exist_ok=True)
    
    return output_path


def save_etf_data_scheduled(use_sample=False):
    """
    Save ETF data to organized folder structure.
    
    Args:
        use_sample (bool): If True, use sample data instead of API
    """
    # Create output folder
    output_path = create_output_folder()
    
    now = datetime.now()
    timestamp = now.strftime('%Y%m%d_%H%M%S')
    
    print("=" * 70)
    print("ETF Data Scheduled Update")
    print("=" * 70)
    print(f"Thời gian cập nhật: {now.strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Thư mục lưu trữ: {output_path}")
    print("=" * 70)
    print()
    
    # Get ETF list
    print("📊 Đang lấy danh sách quỹ ETF...")
    etf_list = get_etf_list(use_sample=use_sample)
    
    if etf_list.empty:
        print("❌ Không tìm thấy dữ liệu ETF")
        return
    
    print(f"✓ Tìm thấy {len(etf_list)} quỹ ETF")
    print()
    
    # Save ETF list to CSV
    list_file = os.path.join(output_path, f'etf_list_{timestamp}.csv')
    etf_list.to_csv(list_file, index=False, encoding='utf-8-sig')
    print(f"✓ Đã lưu danh sách ETF: {list_file}")
    
    # Save to Excel with multiple sheets
    excel_file = os.path.join(output_path, f'etf_data_{timestamp}.xlsx')
    
    try:
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            # Save ETF list
            etf_list.to_excel(writer, sheet_name='ETF_List', index=False)
            print(f"✓ Đã lưu sheet 'ETF_List'")
            
            # Get data for all ETFs
            print()
            print("📈 Đang tải dữ liệu chi tiết cho từng quỹ ETF...")
            
            for idx, row in etf_list.iterrows():
                symbol = row['symbol']
                print(f"  [{idx+1}/{len(etf_list)}] Đang xử lý {symbol}...", end=' ')
                
                try:
                    # Get historical data (last 1 year)
                    historical_data = get_etf_historical_data(
                        symbol,
                        use_sample=use_sample
                    )
                    
                    if not historical_data.empty:
                        # Excel sheet name limit is 31 characters
                        sheet_name = f"{symbol}_Price"[:31]
                        historical_data.to_excel(writer, sheet_name=sheet_name, index=False)
                        print(f"✓ Giá ({len(historical_data)} ngày)", end=' ')
                    
                    # Get fund info
                    fund_info = get_etf_fund_info(symbol, use_sample=use_sample)
                    if not fund_info.empty:
                        # Excel sheet name limit is 31 characters
                        sheet_name = f"{symbol}_Info"[:31]
                        fund_info.to_excel(writer, sheet_name=sheet_name, index=False)
                        print(f"✓ Thông tin quỹ")
                    else:
                        print()
                        
                except Exception as e:
                    print(f"✗ Lỗi: {e}")
                    continue
        
        print()
        print(f"✓ Đã lưu dữ liệu Excel: {excel_file}")
        
    except Exception as e:
        print(f"❌ Lỗi khi lưu Excel: {e}")
    
    print()
    print("=" * 70)
    print("Hoàn thành cập nhật dữ liệu ETF!")
    print("=" * 70)
    
    # Create a summary file
    summary_file = os.path.join(output_path, f'summary_{timestamp}.txt')
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("BÁO CÁO CẬP NHẬT DỮ LIỆU ETF\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Thời gian: {now.strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write(f"Thư mục: {output_path}\n")
        f.write(f"Số lượng ETF: {len(etf_list)}\n\n")
        f.write("Danh sách quỹ ETF:\n")
        f.write("-" * 50 + "\n")
        for idx, row in etf_list.iterrows():
            f.write(f"{idx+1}. {row['symbol']} - {row['organ_name']}\n")
        f.write("\n" + "=" * 50 + "\n")
    
    print(f"✓ Đã tạo báo cáo tóm tắt: {summary_file}")


def main():
    """Main function for scheduled updates."""
    import sys
    
    # Check if --sample flag is provided
    use_sample = "--sample" in sys.argv or "--demo" in sys.argv
    
    if use_sample:
        print("⚠️  Chế độ demo: Sử dụng dữ liệu mẫu")
        print()
    
    save_etf_data_scheduled(use_sample=use_sample)


if __name__ == "__main__":
    main()
