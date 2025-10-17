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

        prompt = f"""
        {data.prompt}のアイテムについて、女性向けに魅力的な商品紹介文を作成してください。
        以下の条件を必ず守ってください：
        -  字数は100〜150文字程度（厳守）
        - 一段落のみで書く
        - 見出し、改行、箇条書きは禁止
        - やさしく親しみやすい言葉で表現
        """

        # 1. 説明文を生成
        text_res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "あなたは手作りアクセサリーの魅力を伝える専門家です。"},
                {"role": "user", "content": prompt}
            ]
        )
        description = text_res.choices[0].message.content

        # 2. 画像を生成
         # GPTに「画像生成用プロンプト」を英語で作らせる
        image_prompt_res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a jewelry photographer."},
                {"role": "user", "content": f"""
次の説明文をもとに、DALL·Eで生成するための英語のプロンプトを作成してください。
人物を含めず、商品単体（白背景 or 明るい背景）を中心に、手作りの質感とデザインがわかる構図にしてください。
説明文: {description}
                """}
            ]
        )
        image_prompt = image_prompt_res.choices[0].message.content.strip()
        print("🎨 image prompt:", image_prompt, flush=True)

        # 3. DALL·Eで生成
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





