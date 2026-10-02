from google import genai
from confidentials import api_key

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="models/gemini-flash-lite-latest",
    contents="Hello"
)

print(response.text)