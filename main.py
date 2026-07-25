import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")


PROMPT = """あなたは新卒採用の面接官です。以下のESを評価してください。

設問: {question}
回答: {answer}
志望業界: {industry}

次の観点で採点(各10点)し、根拠と改善案を示してください。
1. 結論が最初に書かれているか
2. 具体性(数値・固有名詞があるか)
3. 課題と行動の因果が明確か
4. 設問への回答になっているか
5. 志望業界との接続

最後に、改善した文章例を400字で提示してください。"""


def review(question, answer, industry):
    res = client.models.generate_content(
        model=MODEL,
        contents=PROMPT.format(
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
