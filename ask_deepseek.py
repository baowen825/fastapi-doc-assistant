import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    timeout=30.0,
    max_retries=0,
)

question = input("请输入你的问题：")

response = client.chat.completions.create(
    model="deepseek-flash",
    messages=[
    {"role": "user", "content": question}
],
    max_tokens=500,
    extra_body={"thinking": {"type": "disabled"}},
)

print(response.choices[0].message.content)