#!/usr/bin/env python3
import os
import threading
import time

# 導入 LINE Bot 應用
from linebot import app

print("🚀 main.py 已啟動")
print(f"🌍 GAE_ENV: {os.environ.get('GAE_ENV', 'Not set')}")
print(f"📋 GOOGLE_CLOUD_PROJECT: {os.environ.get('GOOGLE_CLOUD_PROJECT', 'Not set')}")

# 只在 GCP 環境中自動更新 Dialogflow
if os.environ.get('GAE_ENV', '').startswith('standard'):
    def update_dialogflow():
        time.sleep(10)
        try:
            from google.cloud import dialogflow_v2 as dialogflow
            from google.protobuf import field_mask_pb2 as field_mask
            import google.auth
            
            # 檢查認證狀態
            credentials, project = google.auth.default()
            print(f'🔐 使用認證: {type(credentials).__name__}')
            print(f'📋 專案 ID: {project}')
            
            # 檢查服務帳戶資訊
            if hasattr(credentials, 'service_account_email'):
                print(f'📧 服務帳戶: {credentials.service_account_email}')
            elif hasattr(credentials, '_service_account_email'):
                print(f'📧 服務帳戶: {credentials._service_account_email}')
            else:
                print('📧 服務帳戶: 無法取得服務帳戶資訊')
            
            project_id = os.environ.get('GOOGLE_CLOUD_PROJECT', project)
            app_url = f"https://{project_id}.appspot.com"
            print(f'🌐 App URL: {app_url}')
            
            # 使用 App Engine 預設服務帳戶 (讓 SDK 自動處理認證)
            client = dialogflow.FulfillmentsClient()
            # 使用動態專案 ID 而不是硬編碼
            dialogflow_project = project_id or 'stinkyturtle-ntnj'
            name = f'projects/{dialogflow_project}/agent/fulfillment'
            print(f'🎯 Dialogflow Agent: {name}')
            
            fulfillment = client.get_fulfillment(name=name)
            print(f'📥 取得 Fulfillment: {fulfillment.name}')
            
            fulfillment.generic_web_service.uri = f"{app_url}/webhook"
            update_mask = field_mask.FieldMask(paths=['generic_web_service.uri'])
            
            client.update_fulfillment(fulfillment=fulfillment, update_mask=update_mask)
            print(f'✅ Dialogflow Webhook 已更新: {app_url}/webhook')
        except Exception as e:
            import traceback
            error_type = type(e).__name__
            print(f'⚠️ Dialogflow 更新失敗 ({error_type}): {e}')
            print(f'📋 詳細錯誤: {traceback.format_exc()}')
            
            # 提供具體的解決建議
            if 'permission' in str(e).lower() or 'forbidden' in str(e).lower():
                print('💡 建議: 檢查 App Engine 服務帳戶是否有 Dialogflow API Admin 權限')
            elif 'not found' in str(e).lower():
                print('💡 建議: 檢查 Dialogflow Agent 是否存在，或專案 ID 是否正確')
            elif 'api' in str(e).lower() and 'not enabled' in str(e).lower():
                print('💡 建議: 在 GCP Console 中啟用 Dialogflow API')
    
    print("🔄 啟動 Dialogflow 更新線程...")
    threading.Thread(target=update_dialogflow, daemon=True).start()
else:
    print("ℹ️  非 GCP 環境，跳過 Dialogflow 更新")

# 導出 app 供 GCP 使用