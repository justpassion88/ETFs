# Quick Reference - ETF Data Updater

## Cài đặt nhanh
```bash
git clone https://github.com/justpassion88/ETFs.git
cd ETFs
pip install -r requirements.txt
```

## Sử dụng cơ bản

### 1. Cập nhật tự động (Scheduled)
```bash
# Chạy cập nhật với lịch định sẵn
python scheduled_update.py

# Hoặc với dữ liệu mẫu (demo)
python scheduled_update.py --sample
```

**Lịch tự động:**
- Chạy mỗi thứ Bảy lúc 6:00 sáng
- Hoặc kích hoạt thủ công từ GitHub Actions

**Dữ liệu lưu tại:**
- Thư mục: `ETF/{ngày}/{tháng}/{năm}/`
- Ví dụ: `ETF/09/02/2026/`

### 2. Cập nhật dữ liệu ETF thủ công
```bash
# Dữ liệu thực (cần kết nối internet)
python update_etf_data.py

# Dữ liệu mẫu (demo)
python update_etf_data.py --sample
```

### 3. Xem ví dụ
```bash
# Chạy tất cả ví dụ
python examples.py --sample
```

### 3. Sử dụng trong Python
```python
from update_etf_data import get_etf_list, get_etf_historical_data

# Lấy danh sách ETF
etfs = get_etf_list()

# Lấy dữ liệu giá
data = get_etf_historical_data('FUEVFVND', '2024-01-01', '2024-12-31')

# In thông tin
print(f"Có {len(etfs)} quỹ ETF")
print(f"Dữ liệu giá có {len(data)} ngày giao dịch")
```

## Các hàm chính

| Hàm | Mô tả | Tham số |
|-----|-------|---------|
| `get_etf_list()` | Lấy danh sách ETF | `use_sample=False` |
| `get_etf_historical_data()` | Lấy giá lịch sử | `symbol, start_date, end_date, use_sample=False` |
| `get_etf_fund_info()` | Lấy thông tin quỹ | `symbol, use_sample=False` |
| `save_etf_data_to_excel()` | Lưu ra Excel | `etf_list, output_file, use_sample=False` |

## Kết quả đầu ra

File `etf_data.xlsx` chứa:
- **ETF_List**: Danh sách tất cả ETF
- **{Symbol}_Price**: Dữ liệu giá từng ETF
- **{Symbol}_Info**: Thông tin quỹ từng ETF

## ETF phổ biến

| Mã | Tên quỹ | Sàn |
|----|---------|-----|
| FUEVFVND | DCVFMVN DIAMOND | HOSE |
| E1VFVN30 | SSIAM VN30 | HOSE |
| FUESSV50 | SSIAM VNFIN LEAD | HOSE |
| FUEVN100 | DCVFMVN VN100 | HOSE |

## Xử lý lỗi

```python
try:
    etf_list = get_etf_list()
    if etf_list.empty:
        print("Không tìm thấy dữ liệu")
except Exception as e:
    print(f"Lỗi: {e}")
```

## Rate Limits

| Loại tài khoản | Requests/phút |
|----------------|---------------|
| Miễn phí | 20 |
| Với API key | 60 |
| Bronze | 180 |
| Silver | 300 |
| Golden | 600 |

## Liên kết hữu ích

- **Thư viện vnstock**: https://github.com/thinh-vu/vnstock
- **Tài liệu Agent Guide**: https://github.com/vnstock-hq/vnstock-agent-guide/
- **Repository này**: https://github.com/justpassion88/ETFs

## Hỗ trợ

Mở issue tại: https://github.com/justpassion88/ETFs/issues

---
© 2026 - ETFs Data Updater using vnstock
