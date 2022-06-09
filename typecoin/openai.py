import os
from urllib.parse import urljoin

from typecoin import network

URL = "https://api.openai.com/v1/"
TOKEN = os.environ["OPEN_AI_API_TOKEN"]


def generate_message(
    prompt: str,
    *,
    model: str = "text-davinci-002",
    temperature: float = 1,
    max_tokens: int = 256,
) -> str:
    payload = {
        "model": model,
        "prompt": prompt + "\n\n",
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    content = network.post(
        urljoin(URL, "completions"), json=payload, bearer_token=TOKEN
    )

    if err := content.get("error"):
        raise RuntimeError(err["message"])

    return content["choices"][0]["text"].strip()
