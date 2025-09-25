import uvicorn
from fastapi import FastAPI, Request
from handlers.webhook_handler import process_webhook_request
from utils.scheduler_utils import start_scheduler
from utils.image_server import setup_image_routes
from config.settings import SEASON_IS_FINISHED

app = FastAPI()

# 設置圖片服務路由
setup_image_routes(app)

# 如果球季未結束，啟動排程器
if not SEASON_IS_FINISHED:
    try:
        scheduler = start_scheduler()
        if scheduler:
            print("✅ 排程器啟動成功")
        else:
            print("⚠️  排程器啟動失敗，但服務器將繼續運行")
    except Exception as e:
        print(f"⚠️  排程器啟動異常: {e}，但服務器將繼續運行")

@app.get("/")
def home():
    return "hello world"

@app.post('/webhook')
async def webhook(request: Request):
    req = await request.json()
    print(req)
    return process_webhook_request(req, SEASON_IS_FINISHED)

def start_server(port=8001):
    """啟動服務器"""
    print(f"🚀 啟動 LINE Bot 服務器在端口 {port}")
    print(f"📱 Webhook URL: http://localhost:{port}/webhook")
    print("⏹️  按 Ctrl+C 停止服務器")
    
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    # 從 local_server 獲取端口配置
    try:
        import local_server
        port = local_server.port
    except:
        port = 8001  # 默認端口
    
    start_server(port)