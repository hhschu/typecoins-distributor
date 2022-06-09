import requests


def generate_message(
    sess: requests.Session,
    prompt: str,
    *,
    temperature: float = 1,
    max_tokens: int = 256,
) -> str:
    payload = {
        "model": "text-davinci-002",
        "prompt": prompt + "\n\n",
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    resp = sess.post("https://api.openai.com/v1/completions", json=payload)
    content = resp.json()

    if err := content.get("error"):
        raise RuntimeError(err["message"])

    return content["choices"][0]["text"].strip()
