# ETFs - Cập nhật dữ liệu quỹ ETF

Dự án cập nhật dữ liệu quỹ ETF (Exchange Traded Fund) thị trường chứng khoán Việt Nam sử dụng thư viện `vnstock`.

## Giới thiệu

Script này tự động lấy và cập nhật dữ liệu các quỹ ETF đang giao dịch trên các sàn chứng khoán Việt Nam (HOSE, HNX, UPCOM).

## Tính năng

- ✅ Lấy danh sách tất cả các quỹ ETF
- ✅ Tải dữ liệu lịch sử giá của ETF
- ✅ Lấy thông tin quỹ (NAV, holdings, performance)
- ✅ Xuất dữ liệu ra file Excel với nhiều sheet
- ✅ Sử dụng thư viện vnstock - miễn phí và dễ sử dụng

## Cài đặt

### Yêu cầu

- Python 3.7 trở lên
- pip (Python package manager)

### Các bước cài đặt

1. Clone repository:
```bash
git clone https://github.com/justpassion88/ETFs.git
cd ETFs
```

2. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

## Sử dụng

### Cách sử dụng cơ bản

**Chế độ thực tế (Lấy dữ liệu từ API):**

Chạy script để cập nhật dữ liệu ETF thực:

```bash
python update_etf_data.py
```

**Chế độ Demo (Sử dụng dữ liệu mẫu):**

Chạy với dữ liệu mẫu để kiểm tra hoặc demo:

```bash
python update_etf_data.py --sample
```

Script sẽ:
1. Lấy danh sách tất cả các quỹ ETF
2. Tải dữ liệu lịch sử giá (1 năm gần nhất)
3. Lấy thông tin quỹ
4. Lưu tất cả dữ liệu vào file `etf_data.xlsx`

### Chạy ví dụ

Xem các ví dụ sử dụng khác nhau:

```bash
# Với dữ liệu thực
python examples.py

# Với dữ liệu mẫu
python examples.py --sample
```

### Sử dụng trong code Python

```python
from update_etf_data import get_etf_list, get_etf_historical_data, get_etf_fund_info

# Lấy danh sách ETF (dữ liệu thực)
etf_list = get_etf_list()
print(etf_list)

# Hoặc dùng dữ liệu mẫu cho demo
etf_list = get_etf_list(use_sample=True)
print(etf_list)

# Lấy dữ liệu lịch sử giá của một ETF cụ thể
historical_data = get_etf_historical_data(
    symbol="FUEVFVND",
    start_date="2024-01-01",
    end_date="2024-12-31"
)
print(historical_data)

# Lấy thông tin quỹ
fund_info = get_etf_fund_info("FUEVFVND")
print(fund_info)
```

## Cấu trúc dữ liệu đầu ra

File Excel `etf_data.xlsx` chứa các sheet:

1. **ETF_List**: Danh sách tất cả các quỹ ETF
2. **{SYMBOL}_Price**: Dữ liệu lịch sử giá của từng ETF
3. **{SYMBOL}_Info**: Thông tin chi tiết của quỹ

## Về thư viện vnstock

`vnstock` là thư viện Python mã nguồn mở để lấy dữ liệu thị trường chứng khoán Việt Nam:

- **Repository**: https://github.com/thinh-vu/vnstock
- **Tài liệu**: https://github.com/vnstock-hq/vnstock-agent-guide/
- **PyPI**: https://pypi.org/project/vnstock/

### Ưu điểm:
- ✅ Miễn phí và mã nguồn mở
- ✅ Dữ liệu đầy đủ và chính xác
- ✅ API đơn giản, dễ sử dụng
- ✅ Hỗ trợ nhiều nguồn dữ liệu (VCI, KBS)
- ✅ Cộng đồng người dùng lớn tại Việt Nam

## Giới hạn sử dụng (Rate Limits)

- **Người dùng miễn phí**: 20 requests/phút
- **Với API key**: 60 requests/phút
- **Tài khoản trả phí**: 180-600 requests/phút

## Xử lý lỗi

Script đã bao gồm xử lý lỗi cơ bản:
- Xử lý khi không có dữ liệu
- Xử lý lỗi kết nối
- Thông báo lỗi rõ ràng

## Đóng góp

Mọi đóng góp đều được chào đón! Vui lòng:
1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

## Tác giả

- GitHub: [@justpassion88](https://github.com/justpassion88)

## Giấy phép

Dự án này được phân phối dưới giấy phép MIT.

## Tài liệu tham khảo

- [vnstock Agent Guide](https://github.com/vnstock-hq/vnstock-agent-guide/)
- [vnstock Documentation](https://docs.vnstock.site/)
- [Vietnamese Stock Market Info](https://vnstocks.com/)
