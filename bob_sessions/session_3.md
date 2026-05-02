/init
Tôi đang xây dựng "ChatOps-Bob Gateway", một microservice FastAPI cho cuộc thi IBM Bob Dev Day Hackathon.
Dự án này ĐÃ CÓ SẴN:
- App FastAPI chạy được trong main.py có CORS và health check
- Cấu hình trong app/core/config.py dùng pydantic-settings
- Môi trường ảo venv/ với Python 3.13
- 27 bài test pytest (nhưng test code cũ, sẽ thay thế)
- File .gitignore đầy đủ
Tôi cần BIẾN ĐỔI dự án thành một cổng ChatOps. Endpoint scan cũ (app/api/v1/endpoints/scan.py và app/schemas/scan.py) là code mẫu tạm, sẽ được thay thế.
Quy tắc kiến trúc:
1. Framework: FastAPI + Pydantic V2 (đã cài sẵn)
2. Database: SQLite bất đồng bộ, CHỈ lưu trong `data/chatops.db`
3. AI Engine: SDK `ibm-watsonx-ai` dùng model `ibm/granite-3-8b-instruct`
4. Mạng xã hội: Telegram Bot qua webhook
5. QUAN TRỌNG: KHÔNG BAO GIỜ ghi file database vào thư mục `bob_sessions/`
6. QUAN TRỌNG: Tất cả phải bất đồng bộ (async), không dùng sync I/O
Hãy cập nhật file AGENTS.md để phản ánh các quy tắc kiến trúc trên.