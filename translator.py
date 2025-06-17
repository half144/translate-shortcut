import requests
import json
from config import Config

class Translator:
    def __init__(self, config=None):
        self.config = config if config is not None else Config()
    
    def translate_text(self, text):
        if not text.strip():
            return text
        
        api_key = self.config.get_api_key()
        if not api_key:
            raise Exception("API key not configured")
        
        target_language = self.config.get_target_language()

        print(f"Target language: {target_language}")
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/user/text-translator",
            "X-Title": "Text Translator MVP"
        }
        
        prompt = (f"Translate the following portuguese text to {target_language}. "
                 f"Rules: "
                 f"1. Preserve slang, expressions, and informal tone exactly as they are "
                 f"2. Maintain original capitalization, punctuation, and formatting "
                 f"3. Keep the natural flow and style of the original text "
                 f"4. If certain expressions don't translate well, use equivalent expressions in {target_language} !important"
                 f"5. ONLY respond with a JSON object in this exact format: {{'translation': 'your translated text here'}} "
                 f"\nText to translate: {text}")
        return self._make_request(headers, prompt, "translation")
    
    def fix_text(self, text):
        if not text.strip():
            return text
        
        api_key = self.config.get_api_key()
        if not api_key:
            raise Exception("API key not configured")
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/user/text-translator",
            "X-Title": "Text Translator MVP"
        }
        
        prompt = (f"Fix any spelling, grammar, or obvious errors in this English text. "
                 f"Keep it natural and conversational - don't make it overly formal. "
                 f"preserve the original capitalization and formatting. !important"
                 f"If the text is already correct, return it unchanged. "
                 f"Only output a json object "
                 f"in the format: {{'corrected': your corrected text here}}: {text}")
        
        return self._make_request(headers, prompt, "corrected")
    
    def _make_request(self, headers, prompt, response_key):
        data = {
            "model": self.config.model,
            "response_format": {"type": "json_object"},
            "max_tokens": 150,
            "temperature": 0.3,
            "messages": [
                {
                    "role": "user", 
                    "content": prompt
                }
            ]
        }
        
        try:
            response = requests.post(
                self.config.openrouter_url,
                headers=headers,
                json=data,
                timeout=8
            )
            
            response.raise_for_status()
            
            result = response.json()
            content = json.loads(result["choices"][0]["message"]["content"])
            
            if response_key not in content:
                raise KeyError(f"A chave '{response_key}' não foi encontrada no JSON de resposta.")
                
            return content[response_key].strip()
            
        except requests.exceptions.HTTPError as e:
            raise Exception(f"API Error: {e.response.status_code} - {e.response.text}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error: {str(e)}")
        except (KeyError, json.JSONDecodeError) as e:
            raise Exception(f"Invalid API response format: {str(e)}")
        except Exception as e:
            raise Exception(f"Processing error: {str(e)}") 