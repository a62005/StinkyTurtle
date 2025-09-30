#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自動更新 Dialogflow Webhook URL
"""
import os
import sys
from google.cloud import dialogflow_v2 as dialogflow
from google.protobuf import field_mask_pb2 as field_mask

def update_dialogflow_webhook(webhook_url, project_id='stinkyturtle-ntnj'):
    """更新 Dialogflow webhook URL"""
    try:
        # 設定認證
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'dialogflow_auth.json'
        
        print(f"🔧 正在更新 Dialogflow Webhook...")
        print(f"📦 專案: {project_id}")
        print(f"🌐 新的 Webhook URL: {webhook_url}")
        
        # 建立 Dialogflow 客戶端
        client = dialogflow.FulfillmentsClient()
        
        # 獲取現有的 fulfillment 設定
        name = f'projects/{project_id}/agent/fulfillment'
        fulfillment = client.get_fulfillment(name=name)
        
        print(f"📋 目前的 Webhook URL: {fulfillment.generic_web_service.uri}")
        
        # 更新 webhook URL
        fulfillment.generic_web_service.uri = webhook_url
        update_mask = field_mask.FieldMask(paths=['generic_web_service.uri'])
        
        # 執行更新
        response = client.update_fulfillment(fulfillment=fulfillment, update_mask=update_mask)
        
        print(f"✅ Dialogflow Webhook 已成功更新!")
        print(f"🎉 新的 Webhook URL: {response.generic_web_service.uri}")
        
        return True
        
    except Exception as e:
        print(f"❌ 更新失敗: {e}")
        print(f"🔍 請檢查:")
        print(f"   1. dialogflow_auth.json 檔案是否存在")
        print(f"   2. 服務帳戶是否有 Dialogflow API 權限")
        print(f"   3. 專案 ID 是否正確: {project_id}")
        return False

def get_gcp_app_url():
    """獲取 GCP App Engine URL"""
    try:
        import subprocess
        result = subprocess.run(['gcloud', 'config', 'get-value', 'project'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            project_id = result.stdout.strip()
            return f"https://{project_id}.appspot.com/webhook"
    except:
        pass
    return None

def main():
    print("🐢 Dialogflow Webhook 更新工具")
    print("=" * 50)
    
    # 嘗試自動獲取 GCP App Engine URL
    auto_url = get_gcp_app_url()
    
    if len(sys.argv) > 1:
        # 從命令列參數獲取 URL
        webhook_url = sys.argv[1]
    elif auto_url:
        # 使用自動檢測的 URL
        print(f"🔍 自動檢測到 GCP App Engine URL: {auto_url}")
        use_auto = input("是否使用此 URL? (y/n): ").lower().strip()
        if use_auto == 'y' or use_auto == 'yes' or use_auto == '':
            webhook_url = auto_url
        else:
            webhook_url = input("請輸入新的 Webhook URL: ").strip()
    else:
        # 手動輸入
        print("請輸入新的 Webhook URL")
        print("例如: https://your-project.appspot.com/webhook")
        webhook_url = input("Webhook URL: ").strip()
    
    if not webhook_url:
        print("❌ 未提供 Webhook URL")
        return
    
    if not webhook_url.startswith('http'):
        print("❌ Webhook URL 必須以 http:// 或 https:// 開頭")
        return
    
    # 執行更新
    success = update_dialogflow_webhook(webhook_url)
    
    if success:
        print("\n🎉 更新完成！")
        print("📝 你可以在 Dialogflow Console 中確認:")
        print("https://dialogflow.cloud.google.com/#/agent/stinkyturtle-ntnj/fulfillment")
    else:
        print("\n❌ 更新失敗，請檢查錯誤訊息")

if __name__ == "__main__":
    main()