from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import traceback
import base64
import google.generativeai as genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("❌ GEMINI_API_KEY が見つかりません")

genai.configure(api_key=api_key)

app = FastAPI()

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
        print("✅ Request:", data.prompt)

        ### ✅ まず説明文を生成
        prompt = f"""
        {data.prompt}のアクセサリーについて、やさしく親しみやすい商品紹介文を作成してください。
        ・100～150文字
        ・改行なし・箇条書き禁止
        """

        text_model = genai.GenerativeModel("gemini-2.0-flash")
        text_res = text_model.generate_content(prompt)
        description = text_res.text.strip()

        print("📝 description:", description)

        ### ✅ Nano Banana 画像生成
        image_model = genai.GenerativeModel("gemini-2.5-flash-image")

        image_prompt = f"""
        Handmade {data.prompt} accessory product photo.
        White soft background, no people, refined and elegant macro shot.
        """

        img_res = image_model.generate_content(image_prompt)

        img_data = img_res.parts[0].inline_data.data
        image_url = f"data:image/png;base64,{img_data}"

        return {
            "description": description,
            "imageUrl": image_url,
        }

    except Exception as e:
        print("⚠️ Gemini API Error:", e)
        traceback.print_exc()
        raise HTTPException(500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
  





