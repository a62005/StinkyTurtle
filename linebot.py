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

@app.get("/test")
def test():
    return {"status": "ok", "message": "Webhook endpoint is working"}

@app.post('/webhook')
async def webhook(request: Request):
    from utils.timezone_utils import format_taipei_time
    
    taipei_time = format_taipei_time()
    print(f"🎯 收到 Webhook 請求 at {taipei_time}")
    try:
        req = await request.json()
        print(f"📨 請求內容: {req}")
        
        # 檢查是否為 Dialogflow 請求
        if 'queryResult' in req:
            intent = req['queryResult']['intent']['displayName']
            query_text = req['queryResult']['queryText']
            print(f"🤖 Dialogflow Intent: {intent}")
            print(f"💬 用戶輸入: {query_text}")
        
        result = process_webhook_request(req, SEASON_IS_FINISHED)
        print(f"📤 回應內容: {result}")
        return result
        
    except Exception as e:
        print(f"❌ Webhook 處理錯誤: {e}")
        import traceback
        print(f"📋 錯誤詳情: {traceback.format_exc()}")
        return {"fulfillmentText": "處理請求時發生錯誤"}

def start_server(port=8080):
    """啟動服務器"""
    print(f"🚀 啟動 LINE Bot 服務器在端口 {port}")
    print(f"📱 Webhook URL: http://localhost:{port}/webhook")
    print("⏹️  按 Ctrl+C 停止服務器")
    
    uvicorn.run(app, port=port)

if __name__ == "__main__":
    # 從 local_server 獲取端口配置
    try:
        import local_server
        port = local_server.port
    except:
        port = 8080  # 默認端口
    
    start_server(port)