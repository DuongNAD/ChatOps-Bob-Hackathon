from app.core.config import settings
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

credentials = Credentials(url=settings.WATSONX_API_URL, api_key=settings.IBM_CLOUD_API_KEY)
model = ModelInference(model_id=settings.WATSONX_MODEL, credentials=credentials, project_id=settings.WATSONX_PROJECT_ID, params={"max_new_tokens": 1024, "decoding_method": "greedy"})

prompt = "You are an expert coding assistant.\n\nUser: hello\nAssistant:"
print(f"PROMPT: {repr(prompt)}")
response = model.generate_text(prompt=prompt)
print("RESPONSE_TYPE:", type(response))
print("RESPONSE_REPR:", repr(response))
