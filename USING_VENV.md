# 🔧 Sử dụng Virtual Environment (venv)

## 📍 Tình trạng hiện tại:

Bạn đang có virtual environment tại: `e:/project/IBM_Hackathon/venv/`

---

## ✅ Đang cài đặt pytest vào venv...

Lệnh đang chạy:
```powershell
C:\Users\DELL\AppData\Local\Programs\Python\Python313\python.exe -m pip install pytest pytest-asyncio pytest-cov httpx
```

---

## 🎯 Sau khi cài đặt xong:

### **Cách 1: Kích hoạt venv và chạy tests**

```powershell
# Kích hoạt venv
.\venv\Scripts\Activate.ps1

# Chạy tests
python -m pytest

# Chạy tests với coverage
python -m pytest --cov=app --cov-report=html

# Thoát venv
deactivate
```

### **Cách 2: Chạy trực tiếp mà không cần kích hoạt venv**

```powershell
# Chạy tests
.\venv\Scripts\python.exe -m pytest

# Chạy tests với coverage
.\venv\Scripts\python.exe -m pytest --cov=app --cov-report=html
```

### **Cách 3: Sử dụng Python system (không dùng venv)**

```powershell
C:\Users\DELL\AppData\Local\Programs\Python\Python313\python.exe -m pytest
```

---

## 🔧 Nếu gặp lỗi "cannot be loaded because running scripts is disabled"

Chạy lệnh này trong PowerShell (với quyền Administrator):

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Sau đó thử lại:
```powershell
.\venv\Scripts\Activate.ps1
```

---

## 📦 Cài đặt thêm packages vào venv:

### **Khi venv đã được kích hoạt:**
```powershell
pip install <package-name>
```

### **Khi venv chưa kích hoạt:**
```powershell
.\venv\Scripts\python.exe -m pip install <package-name>
```

---

## 🎯 Khuyến nghị:

### **Sử dụng venv (Cách tốt nhất):**

1. Kích hoạt venv:
```powershell
.\venv\Scripts\Activate.ps1
```

2. Kiểm tra Python:
```powershell
python --version
# Kết quả: Python 3.13.3
```

3. Cài đặt dependencies:
```powershell
pip install -r requirements.txt
```

4. Chạy tests:
```powershell
pytest
# hoặc
python -m pytest
```

5. Thoát venv khi xong:
```powershell
deactivate
```

---

## 💡 Lợi ích của Virtual Environment:

1. ✅ Tách biệt dependencies giữa các projects
2. ✅ Không ảnh hưởng đến Python system
3. ✅ Dễ dàng quản lý versions
4. ✅ Có thể xóa và tạo lại dễ dàng

---

## 🗑️ Xóa và tạo lại venv (nếu cần):

```powershell
# Xóa venv cũ
Remove-Item -Recurse -Force venv

# Tạo venv mới
C:\Users\DELL\AppData\Local\Programs\Python\Python313\python.exe -m venv venv

# Kích hoạt venv mới
.\venv\Scripts\Activate.ps1

# Cài đặt dependencies
pip install -r requirements.txt

# Chạy tests
pytest
```

---

## 📋 Checklist:

- [ ] pytest đã được cài vào venv (đang chạy)
- [ ] Có thể kích hoạt venv: `.\venv\Scripts\Activate.ps1`
- [ ] Có thể chạy tests: `python -m pytest`
- [ ] Tất cả 30+ tests PASS

---

## 🆘 Vẫn gặp vấn đề?

Xem các file hướng dẫn khác:
- `RUN_TESTS_WITHOUT_PATH.md` - Chạy tests không cần PATH
- `tests/TROUBLESHOOTING.md` - Khắc phục lỗi
- `tests/QUICKSTART.md` - Hướng dẫn nhanh

---

**Made with ❤️ by Bob - Senior QA Engineer**