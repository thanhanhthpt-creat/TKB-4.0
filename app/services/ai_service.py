import json
import logging
import requests
from typing import Any

logger = logging.getLogger(__name__)

class AIService:
    """
    Dịch vụ AI gọi API của Google Gemini.
    Hỗ trợ cơ chế Fallback tự động nếu gặp lỗi:
    1. gemini-3-flash-preview (Mặc định)
    2. gemini-3-pro-preview
    3. gemini-2.5-flash
    """
    MODELS = [
        "gemini-3-flash-preview",
        "gemini-3-pro-preview",
        "gemini-2.5-flash"
    ]

    def __init__(self, api_key: str):
        self.api_key = api_key

    def call_gemini(self, prompt: str, system_instruction: str = "") -> str:
        """
        Gọi API Gemini với cơ chế Fallback.
        Trả về text kết quả hoặc raise Exception nếu tất cả model đều thất bại.
        """
        if not self.api_key:
            raise ValueError("Chưa cấu hình API Key. Vui lòng vào Cài đặt AI để nhập API Key.")

        last_error = None
        for model in self.MODELS:
            try:
                logger.info(f"Đang thử gọi model {model}...")
                return self._call_model(model, prompt, system_instruction)
            except Exception as e:
                logger.warning(f"Model {model} thất bại: {e}")
                last_error = e
        
        raise RuntimeError(f"Tất cả các model đều thất bại. Lỗi cuối: {last_error}")

    def _call_model(self, model: str, prompt: str, system_instruction: str) -> str:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.api_key}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        payload: dict[str, Any] = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ]
        }
        
        if system_instruction:
            payload["systemInstruction"] = {
                "parts": [{"text": system_instruction}]
            }

        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code != 200:
            error_msg = f"HTTP {response.status_code}: {response.text}"
            raise Exception(error_msg)
            
        data = response.json()
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError) as e:
            raise Exception(f"Không thể đọc kết quả từ API trả về: {e}, Response: {data}")
