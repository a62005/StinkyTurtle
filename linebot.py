import uvicorn
from fastapi import FastAPI, Request
from handlers.webhook_handler import process_webhook_request
from utils.scheduler_utils import start_scheduler
from config.settings import SEASON_IS_FINISHED
import local_server

app = FastAPI()

# 如果球季未結束，啟動排程器
if not SEASON_IS_FINISHED:
    start_scheduler()

@app.get("/")
def home():
    return "hello world"

@app.post('/webhook')
async def webhook(request: Request):
    req = await request.json()
    print(req)
    return process_webhook_request(req, SEASON_IS_FINISHED)
uvicorn.run(app, port=local_server.port)