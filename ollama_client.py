from __future__ import annotations
import requests
from typing import Any, Dict, Optional

class OllamaClient:
    def __init__(self, model: str, base_url: str = "http://localhost:11434", timeout_s: int = 60):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout_s = timeout_s

    def ping(self) -> bool:
        #Checks to see if Ollama is reachable
        try:
            r = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return r.status_code == 200
        except Exception:
            return False

    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> str:
        
        #Calls Ollama /api/generate and returns the generated text.
        payload: Dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.4,
                "num_predict": 250,
            },
        }

        if system:
            payload["system"] = system
        if options:
            payload["options"].update(options)

        r = requests.post(f"{self.base_url}/api/generate", json=payload, timeout=self.timeout_s)
        r.raise_for_status()
        return r.json().get("response", "").strip()