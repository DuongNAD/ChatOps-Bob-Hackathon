# 🤖 Kế Hoạch Triển Khai: ChatOps RPA Agent (IBM Hackathon) - V2

> **Chiến lược:** Kết hợp **Bob Shell CLI** (lõi xử lý ổn định) + **RPA pyautogui** (hiệu ứng Demo WOW)

---

## 📋 Tổng Quan Kiến Trúc

```
Telegram (Điện thoại)
    │
    ▼
FastAPI Server (localhost:8000)
    │
    ├── /bob <lệnh>  ──► RPA Controller ──► Điều khiển VS Code ──► Chụp ảnh ──► Gửi ảnh + code về Telegram
    │
    └── Chat bình thường ──► Watsonx AI ──► Trả lời text về Telegram
```

---

## 🛠️ Các Bước Thực Hiện (Copy từng Prompt vào Bob)

### Bước 1: Cài đặt thư viện (5 phút)

Chạy lệnh sau trong Terminal:
```powershell
.\venv\Scripts\pip.exe install pyautogui pillow opencv-python pyperclip --default-timeout=1000
```

Sau đó nhờ Bob cập nhật `requirements.txt`:
> **Prompt Bob:**
> ```
> Thêm các thư viện sau vào file requirements.txt: pyautogui, pillow, opencv-python, pyperclip. Giữ nguyên các thư viện cũ.
> ```

---

### Bước 2: Nâng cấp Telegram Adapter - Gửi ảnh (15 phút)

> **Prompt Bob:**
> ```
> Mở file app/services/channel_adapters/telegram.py.
> Thêm một method mới tên send_photo(self, chat_id: str, photo_path: str, caption: str = "") -> bool.
> Method này gửi ảnh qua Telegram API endpoint /sendPhoto sử dụng multipart/form-data.
> Dùng httpx.AsyncClient với files parameter để upload ảnh.
> Nếu có caption thì gửi kèm caption với parse_mode Markdown.
> Trả về True nếu thành công, False nếu thất bại.
> Giữ nguyên toàn bộ code cũ, chỉ thêm method mới.
> ```

---

### Bước 3: Xây dựng RPA Controller (30 phút) ⭐ QUAN TRỌNG NHẤT

> **Prompt Bob:**
> ```
> Tạo file mới app/services/rpa_controller.py với nội dung sau:
>
> Import: asyncio, logging, os, datetime, pyautogui, pyperclip
>
> Class RPAController:
>   - Thuộc tính: _lock = asyncio.Lock() để chống tranh chấp đa luồng
>   - Thuộc tính: is_busy = False
>   - Thuộc tính: screenshot_dir = "data/screenshots"
>
>   Method __init__:
>     - Tạo thư mục data/screenshots nếu chưa tồn tại
>     - Cấu hình pyautogui.PAUSE = 0.5 và pyautogui.FAILSAFE = True
>
>   Method async execute_bob_command(self, command: str) -> dict:
>     - Trả về dict có keys: success (bool), screenshot_path (str), code_text (str), error (str)
>     - Dùng async with self._lock để đảm bảo chỉ 1 lệnh chạy tại 1 thời điểm
>     - Set self.is_busy = True khi bắt đầu, False khi kết thúc
>     - Gọi await asyncio.to_thread(self._run_rpa, command) để chạy RPA trong thread riêng
>     - Bọc trong try/except, nếu lỗi trả về dict với success=False và error message
>
>   Method _run_rpa(self, command: str) -> dict (sync method, chạy trong thread riêng):
>     - Bước 1: Focus VS Code bằng pyautogui.hotkey('alt', 'tab'), sleep 1s
>     - Bước 2: Mở ô chat Bob bằng phím tắt Ctrl+Shift+I (phím mở Gemini/Bob chat), sleep 1s
>     - Bước 3: Dùng pyperclip.copy(command) rồi pyautogui.hotkey('ctrl', 'v') để dán lệnh, sleep 0.5s
>     - Bước 4: pyautogui.press('enter') để gửi lệnh, sleep 0.5s
>     - Bước 5: Chờ Bob xử lý - time.sleep(25) (có thể điều chỉnh)
>     - Bước 6: Chụp ảnh màn hình toàn bộ bằng pyautogui.screenshot()
>     - Lưu vào data/screenshots/bob_result_{timestamp}.png
>     - Bước 7: Thử lấy code từ clipboard (select all + copy trong panel Bob)
>     - Trả về dict với success=True, screenshot_path, code_text (nếu có)
>
> Thêm logging đầy đủ cho mỗi bước.
> QUAN TRỌNG: Tất cả thao tác pyautogui phải nằm trong method sync _run_rpa, 
> KHÔNG BAO GIỜ gọi trực tiếp trong async method.
> ```

---

### Bước 4: Tích hợp vào Message Router (15 phút)

> **Prompt Bob:**
> ```
> Mở file app/services/message_router.py.
> 
> Import thêm RPAController từ app.services.rpa_controller.
> Import thêm os ở đầu file.
>
> Trong hàm process_incoming_message, TRƯỚC dòng "Step 1: Save user message",
> thêm logic kiểm tra lệnh đặc biệt:
>
> if message.content.startswith("/bob "):
>     # Trích xuất lệnh (bỏ prefix "/bob ")
>     bob_command = message.content[5:].strip()
>     
>     rpa = RPAController()
>     
>     # Kiểm tra nếu đang bận
>     if rpa.is_busy:
>         await telegram_adapter.send_message(
>             chat_id=message.sender_id,
>             text="⏳ Hệ thống đang bận xử lý lệnh khác. Vui lòng đợi..."
>         )
>         return "busy"
>     
>     # Thông báo đang xử lý
>     await telegram_adapter.send_message(
>         chat_id=message.sender_id,
>         text=f"🤖 Đang gửi lệnh cho IBM Bob:\n`{bob_command}`\n\nVui lòng đợi 20-30 giây..."
>     )
>     
>     # Thực thi RPA
>     result = await rpa.execute_bob_command(bob_command)
>     
>     if result["success"]:
>         # Gửi ảnh chụp màn hình
>         if result.get("screenshot_path") and os.path.exists(result["screenshot_path"]):
>             await telegram_adapter.send_photo(
>                 chat_id=message.sender_id,
>                 photo_path=result["screenshot_path"],
>                 caption="📸 Kết quả từ IBM Bob"
>             )
>         
>         # Gửi code text nếu có
>         if result.get("code_text"):
>             await telegram_adapter.send_message(
>                 chat_id=message.sender_id,
>                 text=f"📝 Code:\n```\n{result['code_text'][:3000]}\n```"
>             )
>         else:
>             await telegram_adapter.send_message(
>                 chat_id=message.sender_id,
>                 text="✅ Lệnh đã được gửi cho Bob. Xem ảnh chụp màn hình ở trên."
>             )
>     else:
>         await telegram_adapter.send_message(
>             chat_id=message.sender_id,
>             text=f"❌ Lỗi RPA: {result.get('error', 'Unknown error')}"
>         )
>     
>     return result.get("code_text", "RPA completed")
>
> Giữ nguyên toàn bộ logic cũ cho tin nhắn thường (không bắt đầu bằng /bob).
> ```

---

### Bước 5: Hiệu chỉnh tọa độ & Test (20 phút)

Chạy script sau trong Terminal để tìm tọa độ chuột real-time:
```powershell
.\venv\Scripts\python.exe -c "import pyautogui, time; [print(pyautogui.position()) or time.sleep(1) for _ in range(30)]"
```

Di chuột đến ô chat Bob trong VS Code và ghi lại tọa độ hiện ra. Sau đó điều chỉnh lại trong `rpa_controller.py` nếu cần.

**Test thử:**
1. Đảm bảo server FastAPI đang chạy
2. Đảm bảo ngrok đang chạy
3. Mở VS Code với panel Bob chat hiển thị sẵn
4. Nhắn tin trên Telegram: `/bob Write hello world in Python`

---

## ⚠️ Lưu Ý Quan Trọng Khi Demo

| Vấn đề | Giải pháp |
|--------|-----------|
| Thay đổi độ phân giải (máy chiếu) | Dùng phím tắt thay vì tọa độ cố định |
| Unikey gây lỗi gõ phím | Dùng Clipboard (copy/paste) thay vì gõ từng chữ |
| Server bị treo khi sleep | Chạy RPA trong `asyncio.to_thread()` |
| Nhiều người nhắn cùng lúc | Dùng `asyncio.Lock()` + thông báo "đang bận" |
| Bob chưa code xong đã chụp ảnh | Tăng thời gian delay hoặc kiểm tra thay đổi màn hình |

---

## 🏆 Thứ Tự Ưu Tiên

1. ✅ **Bước 1** - Cài thư viện (bắt buộc)
2. ✅ **Bước 2** - Telegram gửi ảnh (bắt buộc)  
3. ✅ **Bước 3** - RPA Controller (cốt lõi)
4. ✅ **Bước 4** - Tích hợp router (kết nối)
5. ✅ **Bước 5** - Test & hiệu chỉnh (hoàn thiện)
