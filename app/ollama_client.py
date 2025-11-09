"""
ollama_client.py — LLM Interface for Jarvis AI
Developed by: Jotiba Ugale
Purpose:
    Connects to the local Ollama server and communicates with
    the selected Mistral model to generate high-quality responses.
"""

import requests
import json

class OllamaLLM:
    """Handles text generation via Ollama API."""

    def __init__(self, model: str = "mistral", host: str = "http://localhost:11434"):
        """
        Initialize the Ollama client.
        Args:
            model (str): The LLM model name (default: 'mistral').
            host (str): The Ollama server base URL.
        """
        self.model = model
        self.url = f"{host}/api/generate"

    # ======================================================
    # 🧠 Chat Method
    # ======================================================
    def chat(self, prompt: str) -> str:
        """
        Sends a prompt to the Ollama API and returns the model's response.

        Args:
            prompt (str): The full text prompt to send to the model.

        Returns:
            str: The generated response text.
        """
        payload = {"model": self.model, "prompt": prompt}
        headers = {"Content-Type": "application/json"}
        final_text = ""

        try:
            with requests.post(self.url, json=payload, headers=headers, stream=True, timeout=120) as response:
                response.raise_for_status()

                for line in response.iter_lines(decode_unicode=True):
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                        if "response" in data:
                            final_text += data["response"]
                        if data.get("done"):
                            break
                    except json.JSONDecodeError:
                        continue

        except requests.exceptions.ConnectionError:
            return "⚠️ Unable to connect to Ollama. Please ensure it's running (use: `ollama serve`)."
        except requests.exceptions.Timeout:
            return "⚠️ Request timed out. The model took too long to respond."
        except Exception as e:
            return f"⚠️ Unexpected error during LLM generation: {e}"

        return final_text.strip()
