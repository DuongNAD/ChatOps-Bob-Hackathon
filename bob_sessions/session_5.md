Tôi gặp lỗi "IBM Watsonx AI SDK not available. Install with: pip install ibm-watsonx-ai" khi bot Telegram cố gọi AI thật.
Hãy chạy lệnh sau trong terminal để cài thư viện IBM Watsonx AI:
.\venv\Scripts\pip.exe install ibm-watsonx-ai --default-timeout=1000
Sau khi cài xong, tắt server (Ctrl+C) rồi khởi động lại:
.\venv\Scripts\python.exe -m uvicorn main:app --reload