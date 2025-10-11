from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from openai import OpenAI  
import traceback

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

class Prompt(BaseModel):
    prompt: str

@app.post("/api/gpt")
async def gpt_response(data: Prompt):
    try:
        print("✅ /api/gpt にリクエストを受信:", data.prompt)

        # 1. 説明文を生成
        text_res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "あなたは手作りアクセサリーの魅力を伝える専門家です。"},
                {"role": "user", "content": f"以下のアイテムを魅力的に説明してください: {data.prompt}"}
            ]
        )
        description = text_res.choices[0].message.content

        # 2. 画像を生成
        img_res = client.images.generate(
            model="dall-e-3",
            prompt=f"{data.prompt} の手作りアクセサリー風デザイン写真",
            size="1024x1024"
        )
        image_url = img_res.data[0].url

        return {"description": description, "imageUrl": image_url}

    except Exception as e:
        print("⚠️ GPT APIエラー:", e, flush=True)
        print("詳細なエラー情報を出力します", flush=True) 
        traceback.print_exc() 
        raise HTTPException(status_code=500, detail=str(e))
        
# 🔽 Renderが要求するポートでFastAPIを起動
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))  # RenderはPORTを自動設定
    uvicorn.run(app, host="0.0.0.0", port=port)     




