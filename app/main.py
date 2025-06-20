from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os

app = FastAPI()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY environment variable not set. "
        "Please add it to your .env file or environment."
    )

openai.api_key = api_key

class EditRequest(BaseModel):
    title: str
    date: str
    body: str
    link: str

@app.post("/edit")
async def edit(req: EditRequest):
    prompt = (
        "Rewrite the following news body in a casual Gen Z WhatsApp style. "
        "Respond with just the rewritten text.\n\n" + req.body
    )
    try:
        resp = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    new_body = resp.choices[0].message.content.strip()
    formatted = (
        "\U0001F985 Loud Hawk News\n"
        f"\U0001F4E2 *{req.title}*\n"
        f"\U0001F4C5 {req.date}\n"
        f"{new_body}\n"
        f"\U0001F517 [Read more]({req.link})"
    )
    return {"text": formatted}
