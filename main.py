from fastapi import FastAPI
from pydantic import BaseModel
import openai

from pydantic import BaseModel

app = FastAPI()

class UserInput(BaseModel):
    user_input: str


'''# ... (APIキー設定など)'''

# 質問を受け付けるエンドポイント
@app.post("/ask/")
async def ask_question(user_input: UserInput):
    user_question = user_input.user_input

    # ユーザーの質問をダイアログに追加
    history.append({"role": "user", "content": user_question})

    # メッセージ履歴を更新して、OpenAIに問い合わせる
    messages.extend(history)
    response = await openai.ChatCompletion.create(  # 非同期リクエスト
        model="gpt-3.5-turbo",
        messages=messages
    )

    # 応答を抽出して返す
    assistant_response = response['choices'][0]['message']['content']
    
    # ダイアログ履歴を更新
    history.append({"role": "assistant", "content": assistant_response})

    return {"response": assistant_response}

# ... (アプリの起動)


