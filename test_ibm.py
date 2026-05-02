from app.core.config import settings
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

credentials = Credentials(url=settings.WATSONX_API_URL, api_key=settings.IBM_CLOUD_API_KEY)
model = ModelInference(model_id=settings.WATSONX_MODEL, credentials=credentials, project_id=settings.WATSONX_PROJECT_ID)

try:
    response = model.generate_text(prompt="Hello, this is a test.")
    print("RESPONSE:", repr(response))
except Exception as e:
    print("ERROR:", str(e))
