# 🚀 Chạy Tests Mà Không Cần Thêm PATH

## ✅ Python đã hoạt động!

Python của bạn đang ở: `C:\Users\DELL\AppData\Local\Programs\Python\Python313\python.exe`

---

## 📦 Đang cài đặt dependencies...

Lệnh đang chạy:
```powershell
C:\Users\DELL\AppData\Local\Programs\Python\Python313\python.exe -m pip install -r requirements.txt
```

Vui lòng đợi quá trình cài đặt hoàn tất (khoảng 1-2 phút).

---

## 🎯 Sau khi cài đặt xong, chạy tests:

### **Cách 1: Sử dụng đường dẫn đầy đủ**

```powershell
# Chạy tất cả tests
C:\Users\DELL\AppData\Local\Programs\Python\Python313\python.exe -m pytest

# Chạy tests với output chi tiết
C:\Users\DELL\AppData\Local\Programs\Python\Python313\python.exe -m pytest -v

# Chạy tests với coverage
C:\Users\DELL\AppData\Local\Programs\Python\Python313\python.exe -m pytest --cov=app --cov-report=html
```

### **Cách 2: Tạo alias (Khuyến nghị)**

Chạy lệnh này một lần trong PowerShell:
```powershell
Set-Alias python C:\Users\DELL\AppData\Local\Programs\Python\Python313\python.exe
```

Sau đó bạn có thể dùng:
```powershell
python -m pytest
python -m pytest -v
python -m pytest --cov=app --cov-report=html
```

**Lưu ý:** Alias chỉ tồn tại trong phiên PowerShell hiện tại. Khi đóng PowerShell, bạn cần tạo lại alias.

### **Cách 3: Tạo alias vĩnh viễn**

1. Mở PowerShell profile:
```powershell
notepad $PROFILE
```

2. Thêm dòng này vào file:
```powershell
Set-Alias python C:\Users\DELL\AppData\Local\Programs\Python\Python313\python.exe
```

3. Lưu file và đóng notepad

4. Reload profile:
```powershell
. $PROFILE
```

Từ giờ, mỗi khi mở PowerShell, alias sẽ tự động có sẵn!

---

## 📝 Các lệnh hữu ích:

### Kiểm tra Python version:
```powershell
C:\Users\DELL\AppData\Local\Programs\Python\Python313\python.exe --version
```

### Kiểm tra pip version:
```powershell
C:\Users\DELL\AppData\Local\Programs\Python\Python313\python.exe -m pip --version
```

### Cài thêm package:
```powershell
C:\Users\DELL\AppData\Local\Programs\Python\Python313\python.exe -m pip install <package-name>
```

### Xem danh sách packages đã cài:
```powershell
C:\Users\DELL\AppData\Local\Programs\Python\Python313\python.exe -m pip list
```

---

## 🎯 Chạy Tests Ngay Bây Giờ

Sau khi cài đặt dependencies hoàn tất, chạy:

```powershell
C:\Users\DELL\AppData\Local\Programs\Python\Python313\python.exe -m pytest
```

Kết quả mong đợi:
```
================================ test session starts =================================
collected 30 items

tests/test_scan.py::TestScanEndpoint::test_scan_endpoint_success_with_full_request PASSED
tests/test_scan.py::TestScanEndpoint::test_scan_endpoint_success_with_minimal_request PASSED
...
================================ 30 passed in 2.50s =================================
```

---

## 💡 Tại sao không cần thêm PATH?

Khi bạn gọi Python bằng đường dẫn đầy đủ, Windows sẽ chạy trực tiếp file python.exe mà không cần tìm trong PATH. Đây là cách an toàn và luôn hoạt động!

---

## 🔧 Vẫn muốn thêm vào PATH?

Nếu bạn muốn gõ `python` thay vì đường dẫn dài, xem hướng dẫn trong:
- `SETUP_PYTHON_PATH.md` - Hướng dẫn thêm PATH thủ công
- `tests/ADD_PYTHON_TO_PATH.md` - Hướng dẫn chi tiết

---

**Made with ❤️ by Bob - Senior QA Engineer**