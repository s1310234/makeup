import React, { useState } from 'react';

export default function App() {
  const [inputs, setInputs] = useState({
    q1: '',
    q1Privacy: '秘密にしたい',
    q2: '',
    q2Privacy: '秘密にしたい',
    q3: '',
    q3Privacy: '秘密にしたい',
    q4: '', 
    q4Privacy: '秘密にしたい',
    q5: '', 
    q5Privacy: '秘密にしたい',
  });

  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setInputs(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async () => {
    const prompt = `1. ${inputs.q1Privacy}：${inputs.q1}\n2. ${inputs.q2Privacy}：${inputs.q2}\n3. ${inputs.q3Privacy}：${inputs.q3}\n4. ${inputs.q4Privacy}：${inputs.q4}\n5. ${inputs.q5Privacy}：${inputs.q5}\n`;

    setLoading(true);
    try {
  const response = await fetch("http://localhost:3001/api/gpt", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt }),
  });

  if (!response.ok) {
    const errText = await response.text();
    throw new Error(`HTTP ${response.status}: ${errText}`);
  }

  const data = await response.json();
  setResult(data.reply);
} catch (error) {
  setResult(`エラーが発生しました: ${error.message}`);
}

    // try {
    //   const response = await fetch("http://localhost:3001/api/gpt", {
    //     method: "POST",
    //     headers: { "Content-Type": "application/json" },
    //     body: JSON.stringify({ prompt }),
    //   });
    //   if (!response.ok) throw new Error("サーバーエラー");
    //   const data = await response.json();
    //   setResult(data.reply);
    // } catch (error) {
    //   setResult(`エラーが発生しました: ${error.message}`);
    // } finally {
    //   setLoading(false);
    // }
  };

  return (
    <div className="app-container">
      <div className="form-wrapper">
        <h1 className="form-title">Make-up Plan Questionnaire</h1>

        {[1, 2, 3, 4, 5].map(num => (
          <div key={num} className="question-block">
            <label className="question-label">
              {[
                '1. メイクの目的を教えてください。',
                '2. メイクはどのような場面でされますか？',
                '3. お好みのメイクの濃さを教えてください。',
                '4. 普段お使いのアイメイクアイテムについて、アイシャドウ・アイライナー・マスカラ以外に使用しているものがあれば教えてください。',
                '5. なりたい雰囲気やイメージがあれば教えてください。'
              ][num - 1]}
            </label>

            <div className="input-group">
            <select
              className="privacy-select"
              name={`q${num}Privacy`}
              value={inputs[`q${num}Privacy`]}
              onChange={handleChange}
            >
              <option value="秘密にしたい">秘密にしたい</option>
              <option value="秘密にしなくて良い">秘密にしなくて良い</option>
            </select>

            <textarea
              className="answer-textarea"
              name={`q${num}`}
              rows={5}
              placeholder={`例：${[
                '第一印象を良くしたい／写真写りをよくしたい など',
                '職場／学校／パーティ など',
                'ナチュラル／しっかりめ／薄めが好き など',
                '涙袋ライナー／カラーマスカラ／アイプチ など',
                '：〇〇さん風にしたい／清楚な雰囲気にしたい など',
              ][num - 1]}`}
              value={inputs[`q${num}`]}
              onChange={handleChange}
            />
            </div>
          </div>
        ))}

        <button
          className="submit-button"
          onClick={handleSubmit}
          disabled={loading}
        >
          {loading ? '送信中...' : '✨ GPTに送信 ✨'}
        </button>

        {result && (
          <div className="result-box">
            <h2 className="result-title">GPTからの返答:</h2>
            <p className="result-text">{result}</p>
          </div>
        )}
      </div>
    </div>
  );
}


