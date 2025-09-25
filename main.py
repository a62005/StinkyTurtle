#!/usr/bin/env python3
"""
LINE Bot 統一啟動腳本
"""
import os
import sys
import time
import threading
import subprocess
import re
from google.cloud import dialogflow_v2 as dialogflow
from google.protobuf import field_mask_pb2 as field_mask

# 設置環境變數
script_directory = os.path.dirname(os.path.abspath(__file__))
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f'{script_directory}/dialogflow_auth.json'

class TunnelManager:
    def __init__(self, port=8001):
        self.port = port
        self.tunnel_url = None
        self.process = None
        
    def update_dialogflow_callback_url(self, url):
        """更新 Dialogflow webhook URL"""
        try:
            client = dialogflow.FulfillmentsClient()
            name = f'projects/stinkyturtle-ntnj/agent/fulfillment'
            fulfillment = client.get_fulfillment(name=name)
            
            fulfillment.generic_web_service.uri = f"{url}/webhook"
            update_mask = field_mask.FieldMask(paths=['generic_web_service.uri', 'generic_web_service.request_headers'])
            
            response = client.update_fulfillment(fulfillment=fulfillment, update_mask=update_mask)
            print(f'✅ 已更新 Dialogflow Webhook: {url}/webhook')
            return True
        except Exception as e:
            print(f'❌ 更新 Dialogflow 失敗: {e}')
            return False

    def start_tunnel(self):
        """啟動 Cloudflare Tunnel"""
        try:
            print(f"🚀 啟動 Cloudflare Tunnel for port {self.port}...")
            
            # 檢查 cloudflared 是否存在
            check_process = subprocess.run(['which', 'cloudflared'], capture_output=True)
            if check_process.returncode != 0:
                print("❌ 找不到 cloudflared 命令")
                print("📦 請先安裝: brew install cloudflared")
                return None
            
            # 啟動 cloudflared
            self.process = subprocess.Popen(
                ['cloudflared', 'tunnel', '--url', f'http://localhost:{self.port}'],
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
                line = self.process.stdout.readline()
                if line:
                    line = line.strip()
                    print(f"📝 {line}")
                    
                    # 查找 tunnel URL
                    url_match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
                    if url_match:
                        self.tunnel_url = url_match.group()
                        print(f"🎉 Tunnel URL: {self.tunnel_url}")
                        
                        # 保存 URL 到文件
                        with open('.tunnel_url', 'w') as f:
                            f.write(self.tunnel_url)
                        
                        # 更新 Dialogflow
                        self.update_dialogflow_callback_url(self.tunnel_url)
                        
                        print(f"✅ Cloudflare Tunnel 已啟動！")
                        print(f"🔗 URL: {self.tunnel_url}")
                        return self.tunnel_url
                
                if self.process.poll() is not None:
                    print("❌ Cloudflare Tunnel 進程意外退出")
                    break
                    
                time.sleep(0.1)
            
            print("⏰ 超時：未能獲取 Tunnel URL")
            if self.process:
                self.process.terminate()
            return None
            
        except Exception as e:
            print(f"❌ Tunnel 啟動失敗: {e}")
            return None
    
    def stop_tunnel(self):
        """停止 Tunnel"""
        if self.process:
            print("🛑 停止 Cloudflare Tunnel...")
            self.process.terminate()
            self.process.wait()

def start_linebot_server(port=8001):
    """啟動 LINE Bot 服務器"""
    import uvicorn
    from linebot import app
    
    print(f"🚀 啟動 LINE Bot 服務器在端口 {port}")
    print(f"📱 Webhook URL: http://localhost:{port}/webhook")
    print("⏹️  按 Ctrl+C 停止服務器")
    
    uvicorn.run(app, host="0.0.0.0", port=port)

def main():
    """主啟動函數"""
    # 獲取端口配置
    try:
        import local_server
        port = local_server.port
    except:
        port = 8001  # 默認端口
    
    print("🐢 StinkyTurtle LINE Bot 啟動中...")
    print("=" * 50)
    
    # 詢問是否需要啟動 tunnel
    use_tunnel = input("是否需要啟動 Cloudflare Tunnel？(y/N): ").lower().strip()
    
    tunnel_manager = None
    
    if use_tunnel in ['y', 'yes', '是']:
        tunnel_manager = TunnelManager(port)
        
        # 在背景線程中啟動 tunnel
        def start_tunnel_thread():
            tunnel_manager.start_tunnel()
        
        tunnel_thread = threading.Thread(target=start_tunnel_thread, daemon=True)
        tunnel_thread.start()
        
        # 等待 tunnel 啟動
        print("⏳ 等待 Tunnel 啟動...")
        time.sleep(5)  # 給 tunnel 一些時間啟動
    
    try:
        # 啟動 LINE Bot 服務器
        start_linebot_server(port)
    except KeyboardInterrupt:
        print("\n🛑 正在停止服務...")
        if tunnel_manager:
            tunnel_manager.stop_tunnel()
        print("👋 服務已停止，再見！")

if __name__ == "__main__":
    main()