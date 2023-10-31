import uuid

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette import status

from database import DataModel
from services import ChatGPT

router = APIRouter(prefix='')


class User(BaseModel):
    email: str


@router.get('/')
async def read_home():
    return {
        'data': 'Chat GPT API Server for Off-site Learning System !',
    }


@router.post('/token')
def create_token(user: User):
    users_model = DataModel('users')

    record = users_model.select('id', 'email', 'token').where('email', user.email).first()
    if record:
        user_id, email, api_token = record
        if api_token:
            return {'api_token': api_token}
        else:
            new_token = str(uuid.uuid4())
            users_model.where('email', user.email).update({'token': new_token})
            return {'api_token': new_token}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')


@router.get('/models')
async def list_models():
    return {
        'data': ChatGPT().models()
    }


@router.get('/ask')
async def post_question(token: str):
    if token is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='`token` クエリパラメータが必要です')

    users_model = DataModel('users')
    record = users_model.select('id').where('token', token).first()

    if record is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'トークンが不正で認証できません')

    user_id, = record

    # プロンプトを設定
    system_prompt_text = "決して答えを言わずに、ユーザーからの質問に答え、回答を導くためのサポートをしてください。"
    assistant_prompt_text = "回答は、以下の内容を指す。y = x^2 + 5x + 4 を微分すると、y' = 2x + 5 である"
    user_prompt_text = "y = x^2 + 5x + 4 という問題で、微分するとどのような計算で答えが求められる？"

    # ChatGPTにプロンプトを送信し、レスポンスを取得
    chatgpt = ChatGPT()
    response = (chatgpt
                .system_prompt(system_prompt_text)
                .assistant_prompt(assistant_prompt_text)
                .prompt(user_prompt_text)
                .submit())

    # レスポンスからメッセージを抽出
    answer_text = ''.join(choice.message.content for choice in response.choices)

    # レスポンスデータをデータベースに格納
    responses_model = DataModel('responses')
    insert_result = responses_model.insert({
        'user_id': user_id,
        'system_prompt': system_prompt_text,
        'assistant_prompt': assistant_prompt_text,
        'user_prompt': user_prompt_text,
        'chat_gpt_answer': answer_text,
    })

    # データの挿入に失敗した場合はHTTPエラーを返す
    if not insert_result:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to store the response data.")

    return {
        'response': response,
        'message': answer_text,
    }
