"""
Production-grade AI client with proper error handling, retries, and validation.

Supports multiple providers (Gemini, OpenAI) with automatic failover and
detailed error reporting. Never silently degrades - always alerts when AI fails.
"""
import json
import logging
import time
from typing import Dict, Optional

from app.config import settings

logger = logging.getLogger(__name__)


class AIClientError(Exception):
    """Raised when AI client encounters an error"""
    pass


class AIClient:
    """Production AI client with retries and validation"""
    
    def __init__(self):
        self.provider = settings.AI_PROVIDER
        self.max_retries = settings.AI_MAX_RETRIES
        self.timeout = settings.AI_TIMEOUT_SECONDS
        
        if not settings.GEMINI_API_KEY and not settings.OPENAI_API_KEY:
            logger.error("No AI API keys configured! AI features will fail.")
    
    def _call_gemini(self, prompt: str) -> str:
        """Call Gemini API with error handling"""
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=settings.GEMINI_API_KEY)
            
            # Configure generation parameters
            generation_config = {
                "temperature": settings.AI_TEMPERATURE,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 2048,
            }
            
            model = genai.GenerativeModel(
                "gemini-1.5-flash",
                generation_config=generation_config
            )
            
            response = model.generate_content(prompt)
            
            if not response.text:
                raise AIClientError("Empty response from Gemini API")
            
            return response.text
            
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise AIClientError(f"Gemini API error: {str(e)}")
    
    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API with error handling"""
        try:
            from openai import OpenAI
            
            client = OpenAI(
                api_key=settings.OPENAI_API_KEY,
                timeout=self.timeout
            )
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert resume writer. Always return valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=settings.AI_TEMPERATURE,
                response_format={"type": "json_object"},
            )
            
            content = response.choices[0].message.content
            
            if not content:
                raise AIClientError("Empty response from OpenAI API")
            
            return content
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise AIClientError(f"OpenAI API error: {str(e)}")
    
    def _validate_json_response(self, raw_response: str) -> Dict:
        """Validate and parse JSON response"""
        try:
            # Clean response (remove markdown code blocks if present)
            cleaned = raw_response.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()
            
            # Parse JSON
            data = json.loads(cleaned)
            
            if not isinstance(data, dict):
                raise ValueError("Response is not a JSON object")
            
            return data
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON response: {raw_response[:200]}")
            raise AIClientError(f"Invalid JSON response: {str(e)}")
        except Exception as e:
            logger.error(f"Error validating response: {e}")
            raise AIClientError(f"Error validating response: {str(e)}")
    
    def generate_json(self, prompt: str, required_keys: Optional[list] = None) -> Dict:
        """
        Generate JSON response from AI with retries and validation.
        
        Args:
            prompt: The prompt to send to AI
            required_keys: List of required keys in the JSON response
        
        Returns:
            Parsed and validated JSON dict
        
        Raises:
            AIClientError: If AI call fails after all retries
        """
        if not settings.GEMINI_API_KEY and not settings.OPENAI_API_KEY:
            raise AIClientError(
                "No AI API keys configured. Please set GEMINI_API_KEY or OPENAI_API_KEY in .env file."
            )
        
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                logger.info(f"AI request attempt {attempt + 1}/{self.max_retries}")
                
                # Call appropriate provider
                if self.provider == "gemini" and settings.GEMINI_API_KEY:
                    raw_response = self._call_gemini(prompt)
                elif self.provider == "openai" and settings.OPENAI_API_KEY:
                    raw_response = self._call_openai(prompt)
                elif settings.GEMINI_API_KEY:
                    # Fallback to Gemini if OpenAI not configured
                    raw_response = self._call_gemini(prompt)
                else:
                    # Fallback to OpenAI
                    raw_response = self._call_openai(prompt)
                
                # Validate and parse response
                result = self._validate_json_response(raw_response)
                
                # Check required keys
                if required_keys:
                    missing_keys = [key for key in required_keys if key not in result]
                    if missing_keys:
                        raise AIClientError(f"Missing required keys: {missing_keys}")
                
                logger.info("AI request successful")
                return result
                
            except AIClientError as e:
                last_error = e
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                
                if attempt < self.max_retries - 1:
                    # Exponential backoff
                    sleep_time = 2 ** attempt
                    logger.info(f"Retrying in {sleep_time} seconds...")
                    time.sleep(sleep_time)
            
            except Exception as e:
                last_error = AIClientError(f"Unexpected error: {str(e)}")
                logger.error(f"Unexpected error in attempt {attempt + 1}: {e}", exc_info=True)
                
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
        
        # All retries failed
        error_msg = f"AI request failed after {self.max_retries} attempts: {last_error}"
        logger.error(error_msg)
        raise AIClientError(error_msg)


# Global client instance
_client = None


def get_client() -> AIClient:
    """Get or create global AI client instance"""
    global _client
    if _client is None:
        _client = AIClient()
    return _client


def generate_json(prompt: str, required_keys: Optional[list] = None) -> Dict:
    """
    Convenience function for generating JSON from AI.
    
    Raises AIClientError if the request fails.
    """
    client = get_client()
    return client.generate_json(prompt, required_keys)
