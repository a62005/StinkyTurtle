#!/usr/bin/env python3
import os
import threading
import time

# 導入 LINE Bot 應用
from linebot import app

# 只在 GCP 環境中自動更新 Dialogflow
if os.environ.get('GAE_ENV', '').startswith('standard'):
    def update_dialogflow():
        time.sleep(10)
        try:
            from google.cloud import dialogflow_v2 as dialogflow
            from google.protobuf import field_mask_pb2 as field_mask
            
            project_id = os.environ.get('GOOGLE_CLOUD_PROJECT')
            app_url = f"https://{project_id}.appspot.com"
            
            # 使用 App Engine 預設服務帳戶 (無需 JSON 金鑰)
            client = dialogflow.FulfillmentsClient()
            name = f'projects/stinkyturtle-ntnj/agent/fulfillment'
            fulfillment = client.get_fulfillment(name=name)
            
            fulfillment.generic_web_service.uri = f"{app_url}/webhook"
            update_mask = field_mask.FieldMask(paths=['generic_web_service.uri'])
            
            client.update_fulfillment(fulfillment=fulfillment, update_mask=update_mask)
            print(f'✅ Dialogflow Webhook 已更新: {app_url}/webhook')
        except Exception as e:
            print(f'⚠️ Dialogflow 更新失敗: {e}')
    
    threading.Thread(target=update_dialogflow, daemon=True).start()

# 導出 app 供 GCP 使用