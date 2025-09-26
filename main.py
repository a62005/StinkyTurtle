#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GCP App Engine 入口點 - 整合自動服務管理
"""
import os
import sys
import threading
import time
from google.cloud import dialogflow_v2 as dialogflow
from google.protobuf import field_mask_pb2 as field_mask

# 導入 LINE Bot 應用
from linebot import app
from config.settings import USE_LOCAL_IMAGE_SERVER

# 設置環境變數
script_directory = os.path.dirname(os.path.abspath(__file__))
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'dialogflow_auth.json'

class GCPServiceManager:
    def __init__(self):
        self.app_url = None
        self.is_gcp = os.environ.get('GAE_ENV', '').startswith('standard')
        
    def get_app_url(self):
        """獲取 GCP App Engine URL"""
        if self.is_gcp:
            # 在 GCP 環境中，從環境變數獲取 URL
            service = os.environ.get('GAE_SERVICE', 'default')
            version = os.environ.get('GAE_VERSION', 'latest')
            project = os.environ.get('GOOGLE_CLOUD_PROJECT', '')
            
            if project:
                if service == 'default':
                    self.app_url = f"https://{project}.appspot.com"
                else:
                    self.app_url = f"https://{service}-dot-{project}.appspot.com"
            
            print(f"🌐 GCP App Engine URL: {self.app_url}")
            return self.app_url
        return None
    
    def update_dialogflow_webhook(self, url):
        """更新 Dialogflow webhook URL"""
        try:
            client = dialogflow.FulfillmentsClient()
            name = f'projects/stinkyturtle-ntnj/agent/fulfillment'
            fulfillment = client.get_fulfillment(name=name)
            
            webhook_url = f"{url}/webhook"
            fulfillment.generic_web_service.uri = webhook_url
            update_mask = field_mask.FieldMask(paths=['generic_web_service.uri', 'generic_web_service.request_headers'])
            
            response = client.update_fulfillment(fulfillment=fulfillment, update_mask=update_mask)
            print(f'✅ 已更新 Dialogflow Webhook: {webhook_url}')
            return True
        except Exception as e:
            print(f'❌ 更新 Dialogflow 失敗: {e}')
            return False
    
    def setup_webhooks_async(self):
        """在背景設定 webhooks"""
        try:
            # 等待一下讓服務完全啟動
            time.sleep(5)
            
            app_url = self.get_app_url()
            if app_url:
                print("🔧 設定 Webhooks...")
                self.update_dialogflow_webhook(app_url)
                print("✅ Webhook 設定完成")
            else:
                print("⚠️  無法獲取應用 URL，跳過 Webhook 設定")
                
        except Exception as e:
            print(f"❌ Webhook 設定失敗: {e}")
    
    def initialize_services(self):
        """初始化服務"""
        print("🐢 StinkyTurtle LINE Bot 在 GCP 上啟動中...")
        print("=" * 50)
        
        if self.is_gcp:
            print("☁️  運行在 Google Cloud Platform")
            
            # 在背景線程設定 webhooks
            webhook_thread = threading.Thread(target=self.setup_webhooks_async, daemon=True)
            webhook_thread.start()
            
        else:
            print("💻 運行在本地環境")
        
        print("✅ 服務初始化完成")
        print("=" * 50)

# 初始化服務管理器
service_manager = GCPServiceManager()
service_manager.initialize_services()

# 導出 FastAPI 應用供 App Engine 使用
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    
    print(f"🚀 啟動 LINE Bot 服務器在端口 {port}")
    if service_manager.app_url:
        print(f"📱 Webhook URL: {service_manager.app_url}/webhook")
    else:
        print(f"📱 本地 Webhook: http://localhost:{port}/webhook")
    
    uvicorn.run(app, host="0.0.0.0", port=port)