# 🚀 Hướng Dẫn Nhanh: Thêm Python vào PATH

## ✅ Python đã được tìm thấy tại:
```
C:\Users\DELL\AppData\Local\Programs\Python\Python313
C:\Users\DELL\AppData\Local\Programs\Python\Python313\Scripts
```

---

## 🎯 Cách 1: Sử dụng Script Tự Động (Đang chạy)

Script PowerShell đang chờ bạn xác nhận. Trong terminal:

1. Gõ **Y** và nhấn Enter
2. Script sẽ tự động thêm Python vào PATH
3. Đóng và mở lại PowerShell/CMD
4. Chạy: `python --version`

---

## 🎯 Cách 2: Thêm Thủ Công (Nếu script không hoạt động)

### Bước 1: Mở Environment Variables
1. Nhấn `Windows + R`
2. Gõ: `sysdm.cpl` và nhấn Enter
3. Tab "Advanced" → Click "Environment Variables..."

### Bước 2: Chỉnh sửa PATH
1. Trong "System variables", tìm và chọn "Path"
2. Click "Edit..."
3. Click "New" và thêm:
   ```
   C:\Users\DELL\AppData\Local\Programs\Python\Python313
   ```
4. Click "New" lần nữa và thêm:
   ```
   C:\Users\DELL\AppData\Local\Programs\Python\Python313\Scripts
   ```
5. Click OK → OK → OK

### Bước 3: Kiểm tra
1. Đóng tất cả PowerShell/CMD
2. Mở PowerShell/CMD MỚI
3. Chạy:
   ```powershell
   python --version
   ```
   Kết quả: `Python 3.13.3`

---

## 🎯 Cách 3: Sử dụng Lệnh PowerShell Trực Tiếp

Mở PowerShell và chạy:

```powershell
# Copy và paste toàn bộ đoạn này vào PowerShell
$pythonPath = "C:\Users\DELL\AppData\Local\Programs\Python\Python313"
$scriptsPath = "C:\Users\DELL\AppData\Local\Programs\Python\Python313\Scripts"
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
$newPath = "$currentPath;$pythonPath;$scriptsPath"
[Environment]::SetEnvironmentVariable("Path", $newPath, "User")
Write-Host "Done! Please restart PowerShell/CMD" -ForegroundColor Green
```

Sau đó:
1. Đóng PowerShell
2. Mở PowerShell mới
3. Chạy: `python --version`

---

## ✅ Sau khi thêm PATH thành công

### 1. Kiểm tra Python
```powershell
python --version
```
Kết quả: `Python 3.13.3`

### 2. Kiểm tra pip
```powershell
python -m pip --version
```

### 3. Cài đặt dependencies
```powershell
cd e:\project\IBM_Hackathon
python -m pip install -r requirements.txt
```

### 4. Chạy tests
```powershell
python -m pytest
```

hoặc với coverage:
```powershell
python -m pytest --cov=app --cov-report=html
```

---

## 📋 Checklist

- [ ] Python đã được thêm vào PATH
- [ ] Đã đóng và mở lại PowerShell/CMD
- [ ] `python --version` hoạt động → Python 3.13.3
- [ ] `python -m pip --version` hoạt động
- [ ] Đã cài dependencies: `python -m pip install -r requirements.txt`
- [ ] Có thể chạy tests: `python -m pytest`

---

## 🐛 Nếu vẫn gặp lỗi

Xem chi tiết trong:
- `tests/ADD_PYTHON_TO_PATH.md` - Hướng dẫn chi tiết
- `tests/TROUBLESHOOTING.md` - Khắc phục các lỗi khác

---

**Made with ❤️ by Bob**