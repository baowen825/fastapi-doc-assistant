import os
from dotenv import load_dotenv
from openai import OpenAI, APITimeoutError

import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv()
app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ping")
def ping():
    return {"message": "pong"}

class CaseInput(BaseModel):
    title: str
    error: str


@app.post("/cases")
def receive_case(case: CaseInput):
    connection = sqlite3.connect("cases.db")
    cursor = connection.execute(
        "INSERT INTO cases (title, error) VALUES (?, ?)",
        (case.title, case.error),
    )
    connection.commit()
    case_id = cursor.lastrowid
    connection.close()

    return {"id": case_id, "title": case.title, "error": case.error}

@app.get("/cases/{case_id}")
def get_case(case_id: int):
    connection = sqlite3.connect("cases.db")
    cursor = connection.execute(
        "SELECT id, title, error FROM cases WHERE id = ?",
        (case_id,),
    )
    record = cursor.fetchone()
    connection.close()

    if record is None:
        raise HTTPException(status_code=404, detail="排障记录不存在")

    return {"id": record[0], "title": record[1], "error": record[2]}

class QuestionInput(BaseModel):
    question: str


@app.post("/ask")
def ask_question(data: QuestionInput):
    try:
        with OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com",
            timeout=30.0,
            max_retries=0,
        ) as client:
            response = client.chat.completions.create(
                model="deepseek-flash",
                messages=[
                    {"role": "user", "content": data.question}
                ],
                max_tokens=500,
                extra_body={"thinking": {"type": "disabled"}},
            )

        return {"answer": response.choices[0].message.content}

    except APITimeoutError:
        raise HTTPException(
            status_code=504,
            detail="模型响应超时，请稍后重试",
        )