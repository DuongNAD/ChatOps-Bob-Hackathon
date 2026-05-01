# Social Media API Gateway

API Gateway backend application built with FastAPI for social media integration.

## 📋 Features

- ✅ FastAPI framework with async support
- ✅ RESTful API design
- ✅ CORS middleware configured
- ✅ Pydantic data validation
- ✅ Auto-generated API documentation (Swagger UI & ReDoc)
- ✅ Environment-based configuration
- ✅ Structured project layout

## 🏗️ Project Structure

```
IBM_Hackathon/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── __init__.py
│   │       │   └── scan.py          # Scan endpoint
│   │       ├── __init__.py
│   │       └── router.py            # API v1 router
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py                # Application settings
│   ├── models/
│   │   └── __init__.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── scan.py                  # Request/Response schemas
│   ├── services/
│   │   └── __init__.py
│   └── __init__.py
├── tests/
├── .env.example                      # Environment variables example
├── main.py                           # Application entry point
├── requirements.txt                  # Python dependencies
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository** (if applicable)
   ```bash
   cd e:/project/IBM_Hackathon
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   
   On Windows (PowerShell):
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   
   On Windows (Command Prompt):
   ```cmd
   venv\Scripts\activate.bat
   ```
   
   On Linux/Mac:
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create environment file**
   ```bash
   copy .env.example .env
   ```
   
   Edit `.env` file if needed to customize settings.

### Running the Application

**Development mode with auto-reload:**
```bash
python main.py
```

**Or using uvicorn directly:**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The application will start at: `http://localhost:8000`

## 📚 API Documentation

Once the application is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔌 API Endpoints

### Root Endpoint
- **GET** `/` - Health check and service information

### Health Check
- **GET** `/health` - Service health status

### Scan Endpoint
- **POST** `/api/v1/scan` - Initialize scanning sequence

#### Request Body Example:
```json
{
  "url": "https://facebook.com/example",
  "platform": "facebook",
  "data": {
    "user_id": "123456"
  }
}
```

#### Response Example:
```json
{
  "message": "Scanning sequence initialized...",
  "status": "success"
}
```

## 🧪 Testing the API

### Using cURL:
```bash
curl -X POST "http://localhost:8000/api/v1/scan" \
  -H "Content-Type: application/json" \
  -d "{\"url\":\"https://facebook.com/example\",\"platform\":\"facebook\"}"
```

### Using PowerShell:
```powershell
$body = @{
    url = "https://facebook.com/example"
    platform = "facebook"
    data = @{
        user_id = "123456"
    }
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/scan" -Method Post -Body $body -ContentType "application/json"
```

### Using Python requests:
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/scan",
    json={
        "url": "https://facebook.com/example",
        "platform": "facebook",
        "data": {"user_id": "123456"}
    }
)
print(response.json())
```

## ⚙️ Configuration

Configuration is managed through environment variables. See `.env.example` for available options:

- `APP_NAME`: Application name
- `APP_VERSION`: Application version
- `DEBUG`: Enable/disable debug mode
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `API_V1_PREFIX`: API v1 prefix (default: /api/v1)
- `ALLOWED_ORIGINS`: CORS allowed origins

## 📦 Dependencies

- **fastapi**: Modern web framework for building APIs
- **uvicorn**: ASGI server for running FastAPI
- **pydantic**: Data validation using Python type annotations
- **pydantic-settings**: Settings management
- **python-dotenv**: Environment variable management
- **httpx**: HTTP client for async requests
- **python-multipart**: Form data parsing

## 🔧 Development

### Adding New Endpoints

1. Create a new file in `app/api/v1/endpoints/`
2. Define your router and endpoints
3. Add schemas in `app/schemas/`
4. Include the router in `app/api/v1/router.py`

### Project Conventions

- Use async/await for all endpoints
- Define Pydantic schemas for request/response validation
- Follow REST API best practices
- Add proper documentation to endpoints

## 📝 License

This project is part of IBM Hackathon.

## 👥 Author

Senior Backend Developer

---

**Note**: This is a basic setup. For production deployment, consider adding:
- Database integration
- Authentication & Authorization
- Rate limiting
- Logging & Monitoring
- Error handling middleware
- Unit & Integration tests