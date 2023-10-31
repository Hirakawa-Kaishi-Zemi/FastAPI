from fastapi import FastAPI

from database import init_db
from handlers import router

app = FastAPI(debug=True)
app.include_router(router=router)


def main():
    init_db(preinsert=True, drop_if_exists=True)

    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)


if __name__ == '__main__':
    main()
