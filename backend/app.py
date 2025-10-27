from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from google import genai
import traceback
import base64

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("❌ GEMINI_API_KEY が見つかりません。環境変数または .env を確認してください。")

client = genai.Client(api_key=api_key)


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

@app.post("/api/gemini")
async def gemini_response(data: Prompt):
    try:
        print("✅ /api/gemini にリクエストを受信:", data.prompt)

        prompt = f"""
        {data.prompt}のアイテムについて、女性向けに魅力的な商品紹介文を作成してください。
        以下の条件を必ず守ってください：
        -  字数は100〜150文字程度（厳守）
        - 一段落のみで書く
        - 見出し、改行、箇条書きは禁止
        - やさしく親しみやすい言葉で表現
        """

        # 1. 説明文を生成
        text_res = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        description = text_res.text.strip()

        # 画像プロンプト
        image_prompt = f"""
        Handmade cute {data.prompt} accessory.
        No human, no ear, product only.
        Soft light, macro shot, white background, cute pastel tone.
        """

        # 画像生成
        img_res = client.models.generate_images(
            model="gemini-2.5-flash-image",
            prompt=image_prompt,
        )

        image_base64 = img_res.images[0].image_base64
        image_url = f"data:image/png;base64,{image_base64}"

        return {"description": description, "imageUrl": image_url}

    except Exception as e:
        print("⚠️ Gemini APIエラー:", e, flush=True)
        traceback.print_exc() 
        raise HTTPException(status_code=500, detail=str(e))
        
# 🔽 Renderが要求するポートでFastAPIを起動
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))  # RenderはPORTを自動設定
    uvicorn.run(app, host="0.0.0.0", port=port)       





