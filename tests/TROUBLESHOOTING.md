# 🔧 Hướng Dẫn Khắc Phục Lỗi Khi Cài Đặt

## ❌ Lỗi: "pip is not recognized" hoặc "Python was not found"

### 🔍 Nguyên nhân:
Python chưa được cài đặt hoặc chưa được thêm vào PATH của Windows.

### ✅ Giải pháp:

#### **Bước 1: Kiểm tra Python đã được cài đặt chưa**

Mở PowerShell hoặc Command Prompt và thử các lệnh sau:

```powershell
# Thử lệnh 1
python --version

# Thử lệnh 2
python3 --version

# Thử lệnh 3
py --version

# Thử lệnh 4 (nếu dùng Anaconda)
conda --version
```

---

#### **Bước 2: Nếu Python chưa được cài đặt**

##### **Cách 1: Cài đặt từ python.org (Khuyến nghị)**

1. Truy cập: https://www.python.org/downloads/
2. Download Python 3.8 trở lên (khuyến nghị Python 3.11 hoặc 3.12)
3. **QUAN TRỌNG**: Khi cài đặt, tick vào ô **"Add Python to PATH"**
4. Click "Install Now"
5. Sau khi cài xong, mở lại PowerShell/CMD mới và thử lại

##### **Cách 2: Cài đặt từ Microsoft Store**

1. Mở Microsoft Store
2. Tìm "Python 3.12" (hoặc phiên bản mới nhất)
3. Click "Get" để cài đặt
4. Sau khi cài xong, mở lại PowerShell/CMD mới

##### **Cách 3: Sử dụng Anaconda (Cho Data Science)**

1. Download Anaconda: https://www.anaconda.com/download
2. Cài đặt Anaconda
3. Sử dụng Anaconda Prompt thay vì PowerShell

---

#### **Bước 3: Thêm Python vào PATH (Nếu đã cài nhưng vẫn lỗi)**

##### **Cách 1: Tự động (Khuyến nghị)**

1. Gỡ cài đặt Python hiện tại
2. Cài đặt lại và nhớ tick "Add Python to PATH"

##### **Cách 2: Thủ công**

1. Tìm đường dẫn Python (thường là):
   - `C:\Users\<YourUsername>\AppData\Local\Programs\Python\Python312\`
   - `C:\Python312\`

2. Thêm vào PATH:
   - Nhấn `Windows + R`, gõ `sysdm.cpl`
   - Tab "Advanced" → "Environment Variables"
   - Trong "System variables", chọn "Path" → "Edit"
   - Click "New" và thêm:
     - `C:\Users\<YourUsername>\AppData\Local\Programs\Python\Python312\`
     - `C:\Users\<YourUsername>\AppData\Local\Programs\Python\Python312\Scripts\`
   - Click OK và mở lại PowerShell/CMD

---

## 🚀 Sau khi cài đặt Python thành công

### **Bước 1: Kiểm tra lại Python**

```powershell
python --version
# Hoặc
py --version
```

Kết quả mong đợi: `Python 3.x.x`

### **Bước 2: Cài đặt dependencies**

Chọn một trong các lệnh sau (tùy theo lệnh nào hoạt động):

```powershell
# Cách 1: Sử dụng python
python -m pip install -r requirements.txt

# Cách 2: Sử dụng py (Python Launcher)
py -m pip install -r requirements.txt

# Cách 3: Sử dụng pip trực tiếp (nếu đã có trong PATH)
pip install -r requirements.txt

# Cách 4: Sử dụng python3
python3 -m pip install -r requirements.txt

# Cách 5: Nếu dùng Anaconda
conda install --file requirements.txt
# Hoặc
pip install -r requirements.txt
```

### **Bước 3: Nâng cấp pip (Khuyến nghị)**

```powershell
python -m pip install --upgrade pip
```

### **Bước 4: Cài đặt từng package riêng lẻ (Nếu cách trên lỗi)**

```powershell
python -m pip install fastapi==0.109.0
python -m pip install uvicorn[standard]==0.27.0
python -m pip install pydantic==2.5.3
python -m pip install pydantic-settings==2.1.0
python -m pip install pytest==7.4.4
python -m pip install pytest-asyncio==0.23.3
python -m pip install pytest-cov==4.1.0
python -m pip install httpx==0.26.0
python -m pip install python-dotenv==1.0.0
```

---

## 🎯 Chạy Tests sau khi cài đặt thành công

```powershell
# Chạy tests
python -m pytest

# Hoặc
py -m pytest

# Hoặc (nếu pytest đã có trong PATH)
pytest

# Chạy với coverage
python -m pytest --cov=app --cov-report=html
```

---

## 🐛 Các lỗi khác thường gặp

### **Lỗi: "No module named 'pytest'"**

**Giải pháp:**
```powershell
python -m pip install pytest pytest-asyncio pytest-cov
```

### **Lỗi: "No module named 'fastapi'"**

**Giải pháp:**
```powershell
python -m pip install fastapi uvicorn
```

### **Lỗi: "Permission denied"**

**Giải pháp:**
```powershell
# Chạy PowerShell/CMD với quyền Administrator
# Hoặc cài vào user directory
python -m pip install --user -r requirements.txt
```

### **Lỗi: "SSL Certificate Error"**

**Giải pháp:**
```powershell
python -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

---

## 🌟 Sử dụng Virtual Environment (Khuyến nghị)

### **Tạo Virtual Environment:**

```powershell
# Tạo venv
python -m venv venv

# Kích hoạt venv trên Windows PowerShell
.\venv\Scripts\Activate.ps1

# Nếu gặp lỗi execution policy, chạy lệnh này trước:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Hoặc kích hoạt bằng CMD
.\venv\Scripts\activate.bat
```

### **Cài đặt dependencies trong venv:**

```powershell
python -m pip install -r requirements.txt
```

### **Chạy tests trong venv:**

```powershell
pytest
```

### **Thoát venv:**

```powershell
deactivate
```

---

## 📋 Checklist Khắc Phục

- [ ] Python đã được cài đặt (version 3.8+)
- [ ] Python đã được thêm vào PATH
- [ ] Có thể chạy `python --version` hoặc `py --version`
- [ ] pip đã được cài đặt
- [ ] Đã cài đặt tất cả dependencies từ requirements.txt
- [ ] Có thể import pytest: `python -c "import pytest; print(pytest.__version__)"`
- [ ] Có thể chạy pytest: `python -m pytest --version`

---

## 💡 Tips

1. **Luôn sử dụng Virtual Environment** để tránh xung đột packages
2. **Mở lại terminal mới** sau khi cài đặt Python hoặc thay đổi PATH
3. **Chạy PowerShell/CMD với quyền Administrator** nếu gặp lỗi permission
4. **Sử dụng `py` launcher** trên Windows thay vì `python` nếu có nhiều phiên bản Python

---

## 📞 Vẫn gặp vấn đề?

Nếu vẫn gặp lỗi, hãy cung cấp thông tin sau:

1. Kết quả của lệnh: `python --version` hoặc `py --version`
2. Kết quả của lệnh: `python -m pip --version`
3. Hệ điều hành và phiên bản Windows
4. Thông báo lỗi chi tiết

---

**Made with ❤️ by Bob - Senior QA Engineer**