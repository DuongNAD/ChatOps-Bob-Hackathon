# 🔧 Hướng Dẫn Thêm Python vào PATH trên Windows

## 📍 Bạn đã cài Python 3.13.3 - Tuyệt vời!

Bây giờ chúng ta cần thêm Python vào PATH để có thể sử dụng lệnh `python` từ bất kỳ đâu.

---

## 🎯 Cách 1: Thêm PATH Thủ Công (Khuyến nghị)

### **Bước 1: Tìm đường dẫn Python**

Python 3.13.3 của bạn thường được cài ở một trong các vị trí sau:

```
C:\Users\DELL\AppData\Local\Programs\Python\Python313\
C:\Users\DELL\AppData\Local\Programs\Python\Python313\Scripts\
```

Hoặc:

```
C:\Python313\
C:\Python313\Scripts\
```

### **Bước 2: Mở Environment Variables**

1. Nhấn phím `Windows + R` trên bàn phím
2. Gõ: `sysdm.cpl` và nhấn Enter
3. Cửa sổ "System Properties" sẽ mở ra
4. Chọn tab **"Advanced"** (Nâng cao)
5. Click nút **"Environment Variables..."** (Biến môi trường)

### **Bước 3: Chỉnh sửa PATH**

#### **Trong cửa sổ Environment Variables:**

1. Tìm phần **"System variables"** (Biến hệ thống) ở phía dưới
2. Tìm và click chọn biến **"Path"**
3. Click nút **"Edit..."** (Chỉnh sửa)

#### **Trong cửa sổ Edit Environment Variable:**

4. Click nút **"New"** (Mới)
5. Thêm đường dẫn thứ nhất:
   ```
   C:\Users\DELL\AppData\Local\Programs\Python\Python313
   ```

6. Click nút **"New"** (Mới) lần nữa
7. Thêm đường dẫn thứ hai:
   ```
   C:\Users\DELL\AppData\Local\Programs\Python\Python313\Scripts
   ```

8. Click **"OK"** để đóng cửa sổ Edit
9. Click **"OK"** để đóng cửa sổ Environment Variables
10. Click **"OK"** để đóng cửa sổ System Properties

### **Bước 4: Kiểm tra**

1. **QUAN TRỌNG**: Đóng tất cả cửa sổ PowerShell/CMD đang mở
2. Mở PowerShell hoặc CMD **MỚI**
3. Chạy lệnh:

```powershell
python --version
```

Kết quả mong đợi:
```
Python 3.13.3
```

---

## 🎯 Cách 2: Sử dụng PowerShell Script (Nhanh hơn)

### **Bước 1: Mở PowerShell với quyền Administrator**

1. Nhấn `Windows + X`
2. Chọn **"Windows PowerShell (Admin)"** hoặc **"Terminal (Admin)"**

### **Bước 2: Chạy lệnh sau**

```powershell
# Thêm Python vào User PATH
$pythonPath = "C:\Users\DELL\AppData\Local\Programs\Python\Python313"
$scriptsPath = "C:\Users\DELL\AppData\Local\Programs\Python\Python313\Scripts"

$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
$newPath = "$currentPath;$pythonPath;$scriptsPath"
[Environment]::SetEnvironmentVariable("Path", $newPath, "User")

Write-Host "✅ Đã thêm Python vào PATH thành công!" -ForegroundColor Green
Write-Host "⚠️ Vui lòng đóng và mở lại PowerShell/CMD để áp dụng thay đổi" -ForegroundColor Yellow
```

### **Bước 3: Kiểm tra**

1. Đóng PowerShell hiện tại
2. Mở PowerShell/CMD mới
3. Chạy:

```powershell
python --version
```

---

## 🎯 Cách 3: Tìm Đường Dẫn Python Tự Động

Nếu bạn không chắc Python được cài ở đâu, chạy lệnh này trong PowerShell:

```powershell
# Tìm Python
Get-ChildItem -Path "C:\Users\DELL\AppData\Local\Programs\Python\" -Recurse -Filter "python.exe" | Select-Object FullName

# Hoặc tìm trong C:\
Get-ChildItem -Path "C:\" -Recurse -Filter "python.exe" -ErrorAction SilentlyContinue | Select-Object FullName
```

Lệnh này sẽ hiển thị tất cả đường dẫn đến python.exe trên máy bạn.

---

## ✅ Sau khi thêm PATH thành công

### **1. Kiểm tra Python**

```powershell
python --version
# Kết quả: Python 3.13.3
```

### **2. Kiểm tra pip**

```powershell
python -m pip --version
# Kết quả: pip 24.x.x from ...
```

### **3. Cài đặt dependencies cho project**

```powershell
cd e:\project\IBM_Hackathon
python -m pip install -r requirements.txt
```

### **4. Chạy tests**

```powershell
python -m pytest
```

---

## 🐛 Troubleshooting

### **Vấn đề 1: Vẫn báo "python is not recognized"**

**Giải pháp:**
1. Đảm bảo bạn đã **đóng và mở lại** PowerShell/CMD
2. Kiểm tra lại đường dẫn có đúng không
3. Thử khởi động lại máy tính

### **Vấn đề 2: Có nhiều phiên bản Python**

**Giải pháp:**
- Sử dụng Python Launcher: `py --version`
- Chỉ định phiên bản: `py -3.13 --version`

### **Vấn đề 3: Không có quyền chỉnh sửa System Variables**

**Giải pháp:**
- Chỉnh sửa **User variables** thay vì System variables
- Hoặc chạy PowerShell với quyền Administrator

---

## 📋 Checklist

- [ ] Đã tìm được đường dẫn Python (thường là `C:\Users\DELL\AppData\Local\Programs\Python\Python313`)
- [ ] Đã thêm Python vào PATH
- [ ] Đã thêm Scripts vào PATH
- [ ] Đã đóng và mở lại PowerShell/CMD
- [ ] Lệnh `python --version` hoạt động
- [ ] Lệnh `python -m pip --version` hoạt động
- [ ] Đã cài đặt dependencies: `python -m pip install -r requirements.txt`
- [ ] Có thể chạy tests: `python -m pytest`

---

## 🚀 Bước Tiếp Theo

Sau khi thêm PATH thành công, quay lại file `tests/QUICKSTART.md` để:
1. Cài đặt dependencies
2. Chạy tests
3. Xem kết quả

---

## 💡 Tips

1. **Luôn sử dụng `python -m pip`** thay vì chỉ `pip` để đảm bảo đúng phiên bản
2. **Đóng và mở lại terminal** sau khi thay đổi PATH
3. **Sử dụng Virtual Environment** cho mỗi project để tránh xung đột

---

**Made with ❤️ by Bob - Senior QA Engineer**