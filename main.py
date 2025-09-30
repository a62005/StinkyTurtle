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
        print("⏰ Dialogflow 更新線程開始，等待 5 秒...")
        time.sleep(5)
        print("🔄 開始執行 Dialogflow 更新...")
        try:
            print("📦 導入 Dialogflow 模組...")
            from google.cloud import dialogflow_v2 as dialogflow
            print("📦 導入 protobuf 模組...")
            from google.protobuf import field_mask_pb2 as field_mask
            print("📦 導入 google.auth 模組...")
            import google.auth
            from google.auth import compute_engine
            
            print('🔍 開始 Dialogflow 認證檢查...')
            
            # 檢查認證狀態
            credentials, project = google.auth.default()
            print(f'🔐 使用認證類型: {type(credentials).__name__}')
            print(f'📋 專案 ID: {project}')
            
            # 檢查服務帳戶資訊
            if hasattr(credentials, 'service_account_email'):
                print(f'📧 服務帳戶: {credentials.service_account_email}')
            elif hasattr(credentials, '_service_account_email'):
                print(f'📧 服務帳戶: {credentials._service_account_email}')
            else:
                print('📧 服務帳戶: 使用 Compute Engine 預設服務帳戶')
            
            # 檢查認證範圍
            if hasattr(credentials, 'scopes') and credentials.scopes:
                print(f'🔑 認證範圍: {credentials.scopes}')
            
            project_id = os.environ.get('GOOGLE_CLOUD_PROJECT', project)
            app_url = f"https://{project_id}.appspot.com"
            print(f'🌐 App URL: {app_url}')
            
            # 使用 App Engine 預設服務帳戶 (完全無金鑰認證)
            print('🔧 建立 Dialogflow 客戶端...')
            
            # 明確指定專案 ID
            dialogflow_project = 'stinkyturtle-ntnj'  # 使用固定專案 ID
            client = dialogflow.FulfillmentsClient()
            name = f'projects/{dialogflow_project}/agent/fulfillment'
            print(f'🎯 Dialogflow Agent: {name}')
            
            print('📡 嘗試取得 Dialogflow Fulfillment...')
            
            # 先測試基本的 API 連接
            try:
                fulfillment = client.get_fulfillment(name=name)
                print(f'📥 成功取得 Fulfillment: {fulfillment.name}')
                print(f'🔗 目前 Webhook URL: {fulfillment.generic_web_service.uri}')
            except Exception as api_error:
                print(f'❌ API 調用失敗: {api_error}')
                
                # 檢查是否是權限問題
                if '401' in str(api_error):
                    print('🔍 這是認證問題，請檢查以下設定：')
                    print('   1. App Engine 服務帳戶是否有 Dialogflow API Admin 權限')
                    print('   2. Dialogflow API 是否已在專案中啟用')
                    print('   3. Dialogflow Agent 是否存在於此專案中')
                elif '403' in str(api_error):
                    print('🔍 這是權限問題，服務帳戶缺少必要權限')
                elif '404' in str(api_error):
                    print('🔍 找不到 Dialogflow Agent，請檢查專案和 Agent 設定')
                
                raise api_error
            
            fulfillment.generic_web_service.uri = f"{app_url}/webhook"
            update_mask = field_mask.FieldMask(paths=['generic_web_service.uri'])
            
            client.update_fulfillment(fulfillment=fulfillment, update_mask=update_mask)
            print(f'✅ Dialogflow Webhook 已更新: {app_url}/webhook')
        except ImportError as import_error:
            print(f'❌ 模組導入失敗: {import_error}')
            print('💡 可能的原因: requirements.txt 中缺少必要的套件')
        except Exception as e:
            import traceback
            error_type = type(e).__name__
            print(f'⚠️ Dialogflow 更新失敗 ({error_type}): {e}')
            print(f'📋 詳細錯誤: {traceback.format_exc()}')
            
            # 提供具體的解決建議
            if '401' in str(e) or 'authentication' in str(e).lower():
                print('💡 解決方案:')
                print('   1. 前往 https://console.cloud.google.com/iam-admin/iam?project=stinkyturtle-ntnj')
                print('   2. 找到 stinkyturtle-ntnj@appspot.gserviceaccount.com')
                print('   3. 編輯並添加 "Dialogflow API Admin" 角色')
                print('   4. 確保 Dialogflow API 已啟用')
            elif 'permission' in str(e).lower() or 'forbidden' in str(e).lower():
                print('💡 建議: 檢查 App Engine 服務帳戶是否有 Dialogflow API Admin 權限')
            elif 'not found' in str(e).lower():
                print('💡 建議: 檢查 Dialogflow Agent 是否存在，或專案 ID 是否正確')
            elif 'api' in str(e).lower() and 'not enabled' in str(e).lower():
                print('💡 建議: 在 GCP Console 中啟用 Dialogflow API')
        finally:
            print("🏁 Dialogflow 更新線程結束")
    
    print("🔄 啟動 Dialogflow 更新線程...")
    threading.Thread(target=update_dialogflow, daemon=True).start()
else:
    print("ℹ️  非 GCP 環境，跳過 Dialogflow 更新")

# 導出 app 供 GCP 使用