from fastapi import FastAPI

from database import init_db
from handlers import router

app = FastAPI(debug=True)
app.include_router(router=router)


def main():
    # pre_insert: True のとき、サーバー起動時に開発用のアカウントを再生成する
    # drop_if_exists: True のとき、サーバー起動時にデータベースをクリーンアップする(既存データが消失するので注意)
    init_db(pre_insert=True, drop_if_exists=False)

    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)


if __name__ == '__main__':
    main()
