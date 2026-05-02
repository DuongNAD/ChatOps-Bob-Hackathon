# 🧪 Hướng Dẫn Testing Toàn Diện

## 📋 Mục Lục

1. [Cài Đặt Nhanh](#cài-đặt-nhanh)
2. [Chạy Tests](#chạy-tests)
3. [Các Scripts Tiện Ích](#các-scripts-tiện-ích)
4. [Troubleshooting](#troubleshooting)

---

## 🚀 Cài Đặt Nhanh

### Bước 1: Cài đặt dependencies vào venv

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Bước 2: Kiểm tra cài đặt

```powershell
.\venv\Scripts\python.exe -m pytest --version
```

---

## 🎯 Chạy Tests

### Cách 1: Sử dụng Scripts (Dễ nhất)

```powershell
# Chạy tất cả tests
.\run_tests.ps1

# Chạy tests với coverage report
.\run_tests_with_coverage.ps1
```

### Cách 2: Sử dụng venv trực tiếp

```powershell
# Chạy tests
.\venv\Scripts\python.exe -m pytest

# Chạy tests chi tiết
.\venv\Scripts\python.exe -m pytest -v

# Chạy tests với coverage
.\venv\Scripts\python.exe -m pytest --cov=app --cov-report=html
```

### Cách 3: Kích hoạt venv rồi chạy

```powershell
# Kích hoạt venv
.\venv\Scripts\Activate.ps1

# Chạy tests
python -m pytest

# Hoặc
pytest

# Thoát venv
deactivate
```

---

## 📊 Kết Quả Mong Đợi

```
================================ test session starts =================================
platform win32 -- Python 3.13.3, pytest-7.4.4, pluggy-1.3.0
rootdir: e:\project\IBM_Hackathon
configfile: pytest.ini
plugins: asyncio-0.23.3, cov-4.1.0
collected 30 items

tests/test_scan.py::TestScanEndpoint::test_scan_endpoint_success_with_full_request PASSED [  3%]
tests/test_scan.py::TestScanEndpoint::test_scan_endpoint_success_with_minimal_request PASSED [  6%]
tests/test_scan.py::TestScanEndpoint::test_scan_response_status_is_success PASSED [  10%]
...
tests/test_scan.py::TestScanEndpointPerformance::test_scan_multiple_concurrent_requests PASSED [100%]

================================ 30 passed in 2.50s =================================
```

---

## 🛠️ Các Scripts Tiện Ích

### 1. `run_tests.ps1`
Chạy tất cả tests với output chi tiết

```powershell
.\run_tests.ps1
```

### 2. `run_tests_with_coverage.ps1`
Chạy tests và tạo coverage report HTML

```powershell
.\run_tests_with_coverage.ps1
```

Sau khi chạy, mở file `htmlcov/index.html` để xem coverage report.

### 3. `add_python_to_path.ps1`
Tự động thêm Python vào PATH

```powershell
.\add_python_to_path.ps1
```

---

## 📚 Test Cases

### TestScanEndpoint (21 tests)
- ✅ Success scenarios với full và minimal requests
- ✅ Response structure validation
- ✅ Data types validation
- ✅ Enum values validation (SeverityLevel, IssueCategory)
- ✅ Business logic validation
- ✅ Issue details validation
- ✅ Multiple platforms support
- ✅ Complex data structures
- ✅ JSON serialization
- ✅ Content type validation
- ✅ Async operations

### TestScanEndpointEdgeCases (4 tests)
- ✅ Null values handling
- ✅ Empty strings handling
- ✅ Very long URLs
- ✅ Response consistency

### TestScanEndpointPerformance (2 tests)
- ✅ Response time validation
- ✅ Concurrent requests handling

**Tổng cộng: 30+ test cases**

---

## 🔧 Troubleshooting

### Lỗi: "No module named 'pytest'"

**Giải pháp:**
```powershell
.\venv\Scripts\python.exe -m pip install pytest pytest-asyncio pytest-cov
```

### Lỗi: "cannot be loaded because running scripts is disabled"

**Giải pháp:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Lỗi: "No module named 'fastapi'"

**Giải pháp:**
```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Tests fail với import errors

**Giải pháp:**
Đảm bảo chạy tests từ thư mục root của project:
```powershell
cd e:\project\IBM_Hackathon
.\venv\Scripts\python.exe -m pytest
```

---

## 📖 Tài Liệu Bổ Sung

### Hướng dẫn chi tiết:
- `tests/README.md` - Hướng dẫn testing chi tiết
- `tests/QUICKSTART.md` - Hướng dẫn nhanh
- `tests/TROUBLESHOOTING.md` - Khắc phục lỗi chi tiết

### Hướng dẫn setup:
- `USING_VENV.md` - Sử dụng virtual environment
- `RUN_TESTS_WITHOUT_PATH.md` - Chạy tests không cần PATH
- `SETUP_PYTHON_PATH.md` - Thêm Python vào PATH
- `tests/ADD_PYTHON_TO_PATH.md` - Hướng dẫn PATH chi tiết

---

## 💡 Tips & Best Practices

### 1. Luôn sử dụng Virtual Environment
```powershell
# Tạo venv mới nếu cần
python -m venv venv

# Kích hoạt
.\venv\Scripts\Activate.ps1

# Cài dependencies
pip install -r requirements.txt
```

### 2. Chạy tests trước khi commit
```powershell
.\run_tests.ps1
```

### 3. Kiểm tra coverage thường xuyên
```powershell
.\run_tests_with_coverage.ps1
```

### 4. Chạy specific test khi debug
```powershell
.\venv\Scripts\python.exe -m pytest tests/test_scan.py::TestScanEndpoint::test_scan_endpoint_success_with_full_request -v
```

### 5. Sử dụng markers để filter tests
```powershell
# Chỉ chạy async tests
.\venv\Scripts\python.exe -m pytest -m asyncio

# Bỏ qua slow tests
.\venv\Scripts\python.exe -m pytest -m "not slow"
```

---

## 📊 Coverage Report

Sau khi chạy tests với coverage, mở file:
```
htmlcov/index.html
```

Trong browser để xem:
- Line coverage
- Branch coverage
- Missing lines
- Detailed file-by-file analysis

---

## 🎯 Checklist

- [ ] Python đã được cài đặt
- [ ] Virtual environment đã được tạo
- [ ] Dependencies đã được cài vào venv
- [ ] Có thể chạy: `.\venv\Scripts\python.exe -m pytest --version`
- [ ] Tất cả 30+ tests PASS
- [ ] Coverage > 80%

---

## 🆘 Cần Trợ Giúp?

1. Đọc `tests/TROUBLESHOOTING.md` cho các lỗi thường gặp
2. Kiểm tra `tests/README.md` cho hướng dẫn chi tiết
3. Xem `USING_VENV.md` cho vấn đề về virtual environment

---

**Made with ❤️ by Bob - Senior QA Engineer**

*Last updated: 2026-05-02*