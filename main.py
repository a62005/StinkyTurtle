#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GCP App Engine 入口點 - 簡化版
"""
import os
import sys

# 設置環境變數
script_directory = os.path.dirname(os.path.abspath(__file__))
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'dialogflow_auth.json'

# 導入 LINE Bot 應用
from linebot import app

# 檢查是否在 GCP 環境
is_gcp = os.environ.get('GAE_ENV', '').startswith('standard')
project_id = os.environ.get('GOOGLE_CLOUD_PROJECT', 'unknown')

print("🐢 StinkyTurtle LINE Bot 啟動中...")
print("=" * 50)

if is_gcp:
    print("☁️  運行在 Google Cloud Platform")
    print(f"📦 專案 ID: {project_id}")
    
    # 構建應用 URL
    service = os.environ.get('GAE_SERVICE', 'default')
    if service == 'default':
        app_url = f"https://{project_id}.appspot.com"
    else:
        app_url = f"https://{service}-dot-{project_id}.appspot.com"
    
    print(f"🌐 應用 URL: {app_url}")
    print(f"📱 Webhook URL: {app_url}/webhook")
    
    # 延遲更新 Dialogflow（避免阻塞啟動）
    def update_dialogflow_later():
        import time
        from google.cloud import dialogflow_v2 as dialogflow
        from google.protobuf import field_mask_pb2 as field_mask
        
        time.sleep(10)  # 等待服務完全啟動
        try:
            client = dialogflow.FulfillmentsClient()
            name = f'projects/stinkyturtle-ntnj/agent/fulfillment'
            fulfillment = client.get_fulfillment(name=name)
            
            webhook_url = f"{app_url}/webhook"
            fulfillment.generic_web_service.uri = webhook_url
            update_mask = field_mask.FieldMask(paths=['generic_web_service.uri'])
            
            client.update_fulfillment(fulfillment=fulfillment, update_mask=update_mask)
            print(f'✅ Dialogflow Webhook 已更新: {webhook_url}')
        except Exception as e:
            print(f'⚠️  Dialogflow 更新失敗: {e}')
    
    # 在背景執行 Dialogflow 更新
    import threading
    threading.Thread(target=update_dialogflow_later, daemon=True).start()
    
else:
    print("💻 運行在本地環境")

print("✅ 服務初始化完成")
print("=" * 50)

# 導出 FastAPI 應用供 App Engine 使用
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    
    print(f"🚀 啟動 LINE Bot 服務器在端口 {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)