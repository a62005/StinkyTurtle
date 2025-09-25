#!/usr/bin/env python3
"""
獨立的 Cloudflare Tunnel 啟動腳本
"""
from google.cloud import dialogflow_v2 as dialogflow
from google.protobuf import field_mask_pb2 as field_mask
import os
import subprocess
import sys
import time
import re

script_directory = os.path.dirname(os.path.abspath(__file__))
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f'{script_directory}/dialogflow_auth.json'

def update_dialogflow_callback_url(url):
    """更新 Dialogflow webhook URL"""
    try:
        client = dialogflow.FulfillmentsClient()
        name = f'projects/stinkyturtle-ntnj/agent/fulfillment'
        fulfillment = client.get_fulfillment(name=name)
        
        fulfillment.generic_web_service.uri = f"{url}/webhook"
        update_mask = field_mask.FieldMask(paths=['generic_web_service.uri', 'generic_web_service.request_headers'])
        
        response = client.update_fulfillment(fulfillment=fulfillment, update_mask=update_mask)
        print(f'✅ Updated Dialogflow Webhook: {url}/webhook')
        return True
    except Exception as e:
        print(f'❌ Failed to update Dialogflow: {e}')
        return False

def start_cloudflare_tunnel(port):
    """啟動 Cloudflare Tunnel"""
    try:
        print(f"🚀 啟動 Cloudflare Tunnel for port {port}...")
        
        # 檢查 cloudflared 是否存在
        check_process = subprocess.run(['which', 'cloudflared'], capture_output=True)
        if check_process.returncode != 0:
            raise FileNotFoundError("cloudflared not found")
        
        # 啟動 cloudflared
        process = subprocess.Popen(
            ['cloudflared', 'tunnel', '--url', f'http://localhost:{port}'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        print("⏳ 等待 Cloudflare Tunnel 啟動...")
        
        # 等待並獲取 URL
        start_time = time.time()
        timeout = 30
        
        while time.time() - start_time < timeout:
            line = process.stdout.readline()
            if line:
                line = line.strip()
                print(f"📝 {line}")
                
                # 查找 tunnel URL
                url_match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
                if url_match:
                    url = url_match.group()
                    print(f"🎉 Tunnel URL: {url}")
                    
                    # 保存 URL 到文件
                    with open('.tunnel_url', 'w') as f:
                        f.write(url)
                    
                    # 更新 Dialogflow
                    update_dialogflow_callback_url(url)
                    
                    print(f"✅ Cloudflare Tunnel 已啟動！")
                    print(f"🔗 URL: {url}")
                    print("📱 現在可以啟動 LINE Bot: python linebot.py")
                    print("⏹️  按 Ctrl+C 停止 tunnel")
                    
                    # 保持運行
                    try:
                        while True:
                            if process.poll() is not None:
                                print("⚠️  Tunnel 進程意外退出")
                                break
                            time.sleep(1)
                    except KeyboardInterrupt:
                        print("\n🛑 停止 Cloudflare Tunnel...")
                        process.terminate()
                        process.wait()
                    
                    return url
            
            if process.poll() is not None:
                print("❌ Cloudflare Tunnel 進程意外退出")
                break
                
            time.sleep(0.1)
        
        print("⏰ 超時：未能獲取 Tunnel URL")
        process.terminate()
        return None
        
    except FileNotFoundError:
        print("❌ 找不到 cloudflared 命令")
        print("📦 請先安裝: brew install cloudflared")
        return None
    except Exception as e:
        print(f"❌ Tunnel 啟動失敗: {e}")
        return None

if __name__ == "__main__":
    port = 8001
    start_cloudflare_tunnel(port)