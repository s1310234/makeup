# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from dotenv import load_dotenv
# from openai import OpenAI
# import os

# load_dotenv()  # .envファイルからAPIキーを読み込む

# app = Flask(__name__)
# CORS(app)

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# @app.route("/api/gpt", methods=["POST"])
# def generate_plan():
#     data = request.get_json()
#     prompt = data.get("prompt")

#     if not prompt:
#         return jsonify({"error": "プロンプトが空です"}), 400

#     try:
#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo",  # または "gpt-3.5-turbo"
#             messages=[
#                 {"role": "system", "content": "あなたはメイクの専門家です。"},
#                 {"role": "user", "content": prompt}
#             ]
#         )
#         reply = response.choices[0].message.content
#         return jsonify({"reply": reply})

#     except Exception as e:
#         print("❌ GPTエラー:", str(e))
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     app.run(port=3001, debug=True)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from openai import OpenAI  # ← 旧: import openai

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError("❌ OPENAI_API_KEY が見つかりません。環境変数または .env を確認してください。")

client = OpenAI(api_key=api_key)


# FastAPI app 初期化
app = FastAPI()

# CORS ミドルウェア（開発時は * でOK）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI クライアントの初期化（v1.0.0 以降）
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Prompt(BaseModel):
    prompt: str

@app.post("/api/gpt")
async def gpt_response(data: Prompt):
    if not data.prompt:
        raise HTTPException(status_code=400, detail="プロンプトが空です")

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # または gpt-4
            messages=[
                {"role": "system", "content": "あなたはメイクの専門家です。"},
                {"role": "user", "content": data.prompt}
            ]
        )
        return {"reply": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



