# 📋 Hướng Dẫn Chạy Unit Tests

## 📦 Cài Đặt Dependencies

Trước khi chạy tests, bạn cần cài đặt các thư viện cần thiết:

```bash
pip install -r requirements.txt
```

## 🚀 Chạy Tests

### 1. Chạy Tất Cả Tests

```bash
pytest
```

hoặc với output chi tiết hơn:

```bash
pytest -v
```

### 2. Chạy Tests Cho Một File Cụ Thể

```bash
pytest tests/test_scan.py
```

### 3. Chạy Một Test Case Cụ Thể

```bash
pytest tests/test_scan.py::TestScanEndpoint::test_scan_endpoint_success_with_full_request
```

### 4. Chạy Tests Theo Class

```bash
pytest tests/test_scan.py::TestScanEndpoint
```

### 5. Chạy Tests Với Coverage Report

```bash
pytest --cov=app --cov-report=html
```

Sau khi chạy, mở file `htmlcov/index.html` để xem báo cáo coverage chi tiết.

### 6. Chạy Tests Với Output Chi Tiết

```bash
pytest -v -s
```

- `-v`: verbose mode (hiển thị chi tiết từng test)
- `-s`: hiển thị print statements

### 7. Chạy Tests Và Dừng Ở Lỗi Đầu Tiên

```bash
pytest -x
```

### 8. Chạy Tests Với Markers

```bash
pytest -m asyncio
```

## 📊 Test Coverage

### Xem Coverage Report Trong Terminal

```bash
pytest --cov=app --cov-report=term-missing
```

### Tạo Coverage Report HTML

```bash
pytest --cov=app --cov-report=html
```

### Tạo Coverage Report XML (cho CI/CD)

```bash
pytest --cov=app --cov-report=xml
```

## 🎯 Cấu Trúc Tests

```
tests/
├── __init__.py           # Package initialization
├── conftest.py           # Pytest fixtures và configuration
├── test_scan.py          # Unit tests cho /scan endpoint
└── README.md             # File hướng dẫn này
```

## 📝 Test Cases Trong test_scan.py

### TestScanEndpoint (Test chính)
- ✅ `test_scan_endpoint_success_with_full_request` - Test với request đầy đủ
- ✅ `test_scan_endpoint_success_with_minimal_request` - Test với request tối thiểu
- ✅ `test_scan_response_status_is_success` - Kiểm tra status response
- ✅ `test_scan_response_scanned_files_count` - Kiểm tra số file được scan
- ✅ `test_scan_response_issues_found_matches_details_length` - Kiểm tra tính nhất quán
- ✅ `test_scan_response_contains_three_sample_issues` - Kiểm tra số lượng issues
- ✅ `test_scan_issue_details_structure` - Kiểm tra cấu trúc issue details
- ✅ `test_scan_issue_severity_levels_are_valid` - Kiểm tra severity levels hợp lệ
- ✅ `test_scan_issue_categories_are_valid` - Kiểm tra categories hợp lệ
- ✅ `test_scan_issue_line_numbers_are_positive` - Kiểm tra line numbers
- ✅ `test_scan_first_issue_is_security_high` - Kiểm tra issue đầu tiên
- ✅ `test_scan_second_issue_is_performance_medium` - Kiểm tra issue thứ hai
- ✅ `test_scan_third_issue_is_code_style_low` - Kiểm tra issue thứ ba
- ✅ `test_scan_all_issues_have_non_empty_descriptions` - Kiểm tra descriptions
- ✅ `test_scan_all_issues_have_recommendations` - Kiểm tra recommendations
- ✅ `test_scan_endpoint_with_different_platforms` - Test với nhiều platforms
- ✅ `test_scan_endpoint_with_only_url` - Test với chỉ URL
- ✅ `test_scan_endpoint_with_complex_data` - Test với data phức tạp
- ✅ `test_scan_response_json_serializable` - Kiểm tra JSON serialization
- ✅ `test_scan_endpoint_content_type` - Kiểm tra content type
- ✅ `test_scan_endpoint_is_async` - Test async operations

### TestScanEndpointEdgeCases (Edge cases)
- ✅ `test_scan_with_null_values` - Test với null values
- ✅ `test_scan_with_empty_strings` - Test với empty strings
- ✅ `test_scan_with_very_long_url` - Test với URL dài
- ✅ `test_scan_response_consistency` - Test tính nhất quán

### TestScanEndpointPerformance (Performance tests)
- ✅ `test_scan_endpoint_response_time` - Test response time
- ✅ `test_scan_multiple_concurrent_requests` - Test concurrent requests

**Tổng cộng: 30+ test cases**

## 🔧 Pytest Configuration

Tạo file `pytest.ini` trong thư mục root để cấu hình pytest:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --strict-markers
    --tb=short
    --disable-warnings
markers =
    asyncio: marks tests as async tests
    slow: marks tests as slow
    integration: marks tests as integration tests
```

## 🐛 Debug Tests

### Chạy Tests Với Debugger

```bash
pytest --pdb
```

Pytest sẽ dừng lại tại điểm lỗi và mở Python debugger.

### Chạy Tests Với Logging

```bash
pytest --log-cli-level=DEBUG
```

## 📈 Best Practices

1. **Chạy tests trước khi commit code**
   ```bash
   pytest
   ```

2. **Kiểm tra coverage thường xuyên**
   ```bash
   pytest --cov=app --cov-report=term-missing
   ```

3. **Sử dụng fixtures để tái sử dụng code**
   - Xem `conftest.py` để biết các fixtures có sẵn

4. **Viết tests có ý nghĩa**
   - Mỗi test nên test một chức năng cụ thể
   - Tên test nên mô tả rõ ràng điều gì được test

5. **Maintain test independence**
   - Mỗi test nên độc lập, không phụ thuộc vào test khác

## 🔍 Troubleshooting

### Lỗi: "Import pytest could not be resolved"

**Giải pháp:**
```bash
pip install pytest pytest-asyncio pytest-cov httpx
```

### Lỗi: "No module named 'app'"

**Giải pháp:**
Đảm bảo bạn đang chạy pytest từ thư mục root của project:
```bash
cd e:/project/IBM_Hackathon
pytest
```

### Lỗi: "fixture 'test_client' not found"

**Giải pháp:**
Đảm bảo file `conftest.py` tồn tại trong thư mục `tests/`

## 📞 Liên Hệ & Hỗ Trợ

Nếu gặp vấn đề khi chạy tests, vui lòng:
1. Kiểm tra lại các dependencies đã được cài đặt
2. Đảm bảo đang chạy từ đúng thư mục
3. Kiểm tra Python version (khuyến nghị Python 3.8+)

## 📚 Tài Liệu Tham Khảo

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [Coverage.py](https://coverage.readthedocs.io/)

---

**Made with ❤️ by Bob - Senior QA Engineer**