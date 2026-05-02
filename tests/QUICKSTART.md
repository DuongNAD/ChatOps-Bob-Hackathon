# ⚡ Quick Start - Chạy Tests Nhanh

## ⚠️ Lỗi khi cài đặt? Đọc ngay: `tests/TROUBLESHOOTING.md`

## 🚀 Các Lệnh Thường Dùng

### 1️⃣ Cài đặt dependencies

**Chọn một trong các lệnh sau (tùy hệ thống):**

```bash
# Cách 1: Sử dụng python (Khuyến nghị)
python -m pip install -r requirements.txt

# Cách 2: Sử dụng py (Python Launcher trên Windows)
py -m pip install -r requirements.txt

# Cách 3: Sử dụng pip trực tiếp
pip install -r requirements.txt

# Cách 4: Sử dụng python3 (Linux/Mac)
python3 -m pip install -r requirements.txt
```

**❌ Nếu gặp lỗi "pip is not recognized" hoặc "Python was not found":**
👉 Xem hướng dẫn chi tiết trong file `tests/TROUBLESHOOTING.md`

### 2️⃣ Chạy tất cả tests

```bash
# Cách 1: Sử dụng python -m (Khuyến nghị)
python -m pytest

# Cách 2: Sử dụng py (Windows)
py -m pytest

# Cách 3: Sử dụng pytest trực tiếp
pytest
```

### 3️⃣ Chạy tests với coverage

```bash
python -m pytest --cov=app --cov-report=html
```

### 4️⃣ Chạy tests chi tiết

```bash
python -m pytest -v
```

### 5️⃣ Chạy một test cụ thể

```bash
python -m pytest tests/test_scan.py::TestScanEndpoint::test_scan_endpoint_success_with_full_request
```

## 📊 Kết Quả Mong Đợi

Khi chạy `pytest`, bạn sẽ thấy:
```
================================ test session starts =================================
collected 30 items

tests/test_scan.py::TestScanEndpoint::test_scan_endpoint_success_with_full_request PASSED
tests/test_scan.py::TestScanEndpoint::test_scan_endpoint_success_with_minimal_request PASSED
...
================================ 30 passed in 2.50s =================================
```

## ✅ Checklist Trước Khi Commit

- [ ] Chạy `python -m pytest` - tất cả tests phải PASS
- [ ] Chạy `python -m pytest --cov=app` - coverage > 80%
- [ ] Không có warnings hoặc errors

## 🆘 Gặp Vấn Đề?

- ❌ **Lỗi cài đặt Python/pip?** → Xem `tests/TROUBLESHOOTING.md`
- ❌ **Lỗi khi chạy tests?** → Xem `tests/README.md` phần Troubleshooting
- ❌ **Import errors?** → Đảm bảo đã cài đặt đầy đủ dependencies

## 📖 Xem Thêm

Đọc file `tests/README.md` để biết thêm chi tiết về:
- Các test cases cụ thể
- Cách debug tests
- Best practices
- Troubleshooting

---
**Made with ❤️ by Bob**