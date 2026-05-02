"""
IBM Watsonx AI client for generating AI responses.

This module provides an interface to IBM Watsonx AI's Granite model
with support for mock mode during development and testing.
"""

import logging
from typing import Optional

from app.core.config import settings

# Configure logging
logger = logging.getLogger(__name__)


class IBMAIClient:
    """
    Client for interacting with IBM Watsonx AI.
    
    Supports both mock mode (for development/testing) and real API calls
    to IBM Watsonx AI using the Granite model.
    """
    
    def __init__(self):
        """Initialize the IBM AI client with settings from configuration."""
        self.use_mock = settings.USE_MOCK_AI
        self.model_id = settings.WATSONX_MODEL
        self.api_url = settings.WATSONX_API_URL
        self.project_id = settings.WATSONX_PROJECT_ID
        self.api_key = settings.IBM_CLOUD_API_KEY
        
        if not self.use_mock:
            logger.info(f"IBM AI Client initialized with model: {self.model_id}")
        else:
            logger.info("IBM AI Client initialized in MOCK mode")
    
    async def generate_response(self, prompt: str, context: str = "") -> str:
        """
        Generate an AI response based on the prompt and optional context.
        
        Args:
            prompt: The user's question or request
            context: Optional conversation context or history
            
        Returns:
            str: The AI-generated response
            
        Note:
            If USE_MOCK_AI is True, returns a fixed mock response.
            Otherwise, calls IBM Watsonx AI API.
        """
        # MOCK MODE - Return fixed response for development/testing
        if self.use_mock:
            logger.debug("Generating mock AI response")
            return self._generate_mock_response()
        
        # REAL MODE - Call IBM Watsonx AI API
        try:
            return await self._generate_real_response(prompt, context)
        except Exception as e:
            logger.error(f"Failed to generate AI response: {e}")
            return self._generate_error_response(str(e))
    
    def _generate_mock_response(self) -> str:
        """
        Generate a fixed mock response for testing.
        
        Returns:
            str: A markdown-formatted mock response
        """
        return (
            "**[Mock AI Response]**\n\n"
            "I have analyzed your request. Here are my suggestions:\n"
            "- Check line 42, there may be an error\n"
            "- Consider adding exception handling\n\n"
            "_Mock mode is ON. Set USE_MOCK_AI=False to use real IBM Granite._"
        )
    
    async def _generate_real_response(self, prompt: str, context: str) -> str:
        """
        Generate a real response using IBM Watsonx AI API.
        
        Args:
            prompt: The user's question or request
            context: Optional conversation context or history
            
        Returns:
            str: The AI-generated response from IBM Granite model
            
        Raises:
            Exception: If API call fails
        """
        try:
            # Import IBM Watsonx AI SDK
            from ibm_watsonx_ai import Credentials
            from ibm_watsonx_ai.foundation_models import ModelInference
            
            # Initialize credentials
            credentials = Credentials(
                url=self.api_url,
                api_key=self.api_key
            )
            
            # Initialize model
            model = ModelInference(
                model_id=self.model_id,
                credentials=credentials,
                project_id=self.project_id,
                params={
                    "max_new_tokens": 1024,
                    "decoding_method": "greedy"
                }
            )
            
            # Create system prompt
            system_prompt = (
                "You are a professional programming assistant. "
                "Help developers debug and improve their code. "
                "CRITICAL: You MUST ALWAYS respond in ENGLISH, regardless of the language used in the user's question. "
                "Even if the user asks in Vietnamese, Chinese, or any other language, you MUST respond in English. "
                "Use appropriate technical terminology and provide clear, professional explanations in English."
            )
            
            # Combine prompts
            full_prompt = f"{system_prompt}\n\n"
            if context:
                full_prompt += f"Context:\n{context}\n\n"
            full_prompt += f"User: {prompt}\nAssistant:"
            
            logger.debug(f"Sending prompt to IBM Watsonx AI: {full_prompt[:100]}...")
            
            # Generate response
            response = model.generate_text(prompt=full_prompt)
            
            logger.info("Successfully generated AI response from IBM Watsonx AI")
            return response
            
        except ImportError as e:
            logger.error(f"IBM Watsonx AI SDK not installed: {e}")
            raise Exception(
                "IBM Watsonx AI SDK not available. "
                "Install with: pip install ibm-watsonx-ai"
            )
        except Exception as e:
            logger.error(f"Error calling IBM Watsonx AI API: {e}")
            raise
    
    def _generate_error_response(self, error_message: str) -> str:
        """
        Generate an error response when API call fails.
        
        Args:
            error_message: The error message to include
            
        Returns:
            str: A user-friendly error message
        """
        return (
            "**[AI Error]**\n\n"
            f"Sorry, an error occurred while processing your request:\n"
            f"```\n{error_message}\n```\n\n"
            "Please try again later or contact the administrator."
        )


# Made with Bob