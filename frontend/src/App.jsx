import './App.css';
import React, { useState } from "react";

export default function App() {
  const questions = [
    {
      text: "1. 今日の気分に一番近いのは？",
      options: [
        "元気いっぱいで華やかにしたい",
        "落ち着いてシンプルに過ごしたい",
        "優雅で女性らしくなりたい",
        "クールにかっこよく見せたい",
        "可愛らしく柔らかい雰囲気にしたい",
      ],
    },
    {
      text: "2. アクセサリーを身につけたいシーンは？",
      options: [
        "仕事や学校でさりげなく",
        "デートやお出かけで華やかに",
        "友人とのカジュアルな集まり",
        "特別なイベントや記念日",
      ],
    },
    {
      text: "3. 普段のファッションに近いテイストは？",
      options: [
        "シンプル＆ベーシック",
        "ガーリー＆キュート",
        "ナチュラル＆リラックス",
        "モード＆個性派",
        "エレガント＆クラシック",
      ],
    },
    {
      text: "4. 今の気分に一番しっくりくる色は？（直感で！）",
      options: [
        "レッド系（情熱・華やか）",
        "ブルー系（落ち着き・知的）",
        "グリーン系（自然・さわやか）",
        "イエロー系（元気・明るさ）",
        "パープル系（ミステリアス・上品）",
      ],
    },
    {
      text: "5. 身につけたいアイテムはどれ？",
      options: [
        "イヤリング",
        "ブレスレット",
        "ブローチ",
        "まだ決めていない（提案してほしい）",
      ],
    },
  ];

  const [inputs, setInputs] = useState({
    q1: "",
    q2: "",
    q3: "",
    q4: "",
    q5: "",
  });

  const [result, setResult] = useState({ description: "", imageUrl: "" });
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setInputs((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async () => {
    const prompt = questions
      .map(
        (q, i) =>
          `${i + 1}. ${q.text}\n回答: ${inputs[`q${i + 1}`] || "未回答"}`
      )
      .join("\n\n");

    setLoading(true);
    try {
      const response = await fetch("https://makeup-3jf5.onrender.com/api/gpt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });

      if (!response.ok) {
        const errText = await response.text();
        throw new Error(`HTTP ${response.status}: ${errText}`);
      }

      const data = await response.json();
      console.log("サーバーからの返答:", data);
      setResult({
        description: data.description,
        imageUrl: data.imageUrl,
      });
    } catch (error) {
      setResult({ description: `エラー: ${error.message}`, imageUrl: "" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="form-wrapper">
        <h1 className="form-title">アクセサリー診断アンケート</h1>

        {questions.map((q, i) => (
          <div key={i} className="question-block">
            <p className="question-label">{q.text}</p>
            <div className="options-group">
              {q.options.map((opt, j) => (
                <label key={j} className="option-label">
                  <input
                    type="radio"
                    name={`q${i + 1}`}
                    value={opt}
                    checked={inputs[`q${i + 1}`] === opt}
                    onChange={handleChange}
                  />
                  {opt}
                </label>
              ))}
            </div>
          </div>
        ))}

        <button
          className="submit-button"
          onClick={handleSubmit}
          disabled={loading}
        >
          {loading ? "送信中..." : "✨ GPTに送信 ✨"}
        </button>

        {result.description && (
          <div className="result-box">
            <h2 className="result-title">生成結果:</h2>
            <p className="result-text">{result.description}</p>
            {result.imageUrl && (
              <img
                src={result.imageUrl}
                alt="生成されたアクセサリー"
                className="result-image"
              />
            )}
          </div>
        )}
      </div>
    </div>
  );
}


