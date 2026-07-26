import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")


PROMPTS = {
    "A_採点型": """あなたは新卒採用の面接官です。（今の内容をそのまま）""",

    "B_役割強化型": """あなたは{industry}業界の大手企業で10年間新卒採用を担当し、
年間3000通のESを読んできた面接官です。
以下のESを、実際の選考と同じ基準で評価してください。

設問: {question}
回答: {answer}

まず全体の第一印象を1行で述べ、次に通過/ボーダー/不通過のいずれかを明示し、
その判断根拠を3点挙げてください。最後に改善案を400字で示してください。""",

    "C_思考手順指定型": """以下のESを評価します。必ずこの順序で考えてください。

設問: {question}
回答: {answer}
志望業界: {industry}

手順1: 回答から「事実」と「主観的な表現」を分けて列挙する
手順2: 事実のうち、数値・固有名詞を伴うものがいくつあるか数える
手順3: 手順1〜2を根拠に、5観点を各10点で採点する
手順4: 最も点数の低い観点に絞って改善案を400字で示す

手順1から順に、思考過程も含めて出力してください。""",
}

def review(question, answer, industry, prompt_key="A_採点型"):
    res = client.models.generate_content(
        model=MODEL,
        contents=PROMPTS[prompt_key].format(
            question=question, answer=answer, industry=industry
        ),
    )
    return res.text



if __name__ == "__main__":
    print(review(
        "学生時代に力を入れたこと",
        "サークルの代表として、メンバーの意識を高めました。",
        "AI・IT"
    ))

import csv
from datetime import datetime

HISTORY_FILE = "history.csv"

def save_history(question, answer, industry, result):
    is_new = not os.path.exists(HISTORY_FILE)
    with open(HISTORY_FILE, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(["日時", "業界", "設問", "回答", "結果"])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            industry, question, answer, result
        ])

