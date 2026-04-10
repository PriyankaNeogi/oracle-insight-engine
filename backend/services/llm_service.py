from openai import OpenAI
from backend.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def generate(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",   # you can move this into config later
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content