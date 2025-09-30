#!/usr/bin/env python3
import os
import threading
import time

# 設置環境變數
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'dialogflow_auth.json'

# 導入 LINE Bot 應用
from linebot import app

# 檢查是否在 GCP 環境
is_gcp = os.environ.get('GAE_ENV', '').startswith('standard')
project_id = os.environ.get('GOOGLE_CLOUD_PROJECT', 'unknown')

if is_gcp:
    # 構建應用 URL
    service = os.environ.get('GAE_SERVICE', 'default')
    app_url = f"https://{project_id}.appspot.com" if service == 'default' else f"https://{service}-dot-{project_id}.appspot.com"
    
    # 自動更新 Dialogflow
    def update_dialogflow():
        time.sleep(10)
        try:
            from google.cloud import dialogflow_v2 as dialogflow
            from google.protobuf import field_mask_pb2 as field_mask
            
            if 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ:
                del os.environ['GOOGLE_APPLICATION_CREDENTIALS']
            
            client = dialogflow.FulfillmentsClient()
            name = f'projects/stinkyturtle-ntnj/agent/fulfillment'
            fulfillment = client.get_fulfillment(name=name)
            
            webhook_url = f"{app_url}/webhook"
            fulfillment.generic_web_service.uri = webhook_url
            update_mask = field_mask.FieldMask(paths=['generic_web_service.uri'])
            
            client.update_fulfillment(fulfillment=fulfillment, update_mask=update_mask)
            print(f'✅ Dialogflow Webhook 已更新: {webhook_url}')
        except Exception as e:
            print(f'⚠️ Dialogflow 更新失敗: {e}')
    
    threading.Thread(target=update_dialogflow, daemon=True).start()

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)