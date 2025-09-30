#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LINE Bot 自動啟動腳本 - 全自動版
自動檢測是否需要啟動 tunnel，然後啟動服務
"""
import os
import sys
import time
import threading
import subprocess
import re
import uvicorn
# 移除 Dialogflow 導入 (認證檔案已被禁用)

# 導入 LINE Bot 應用
from linebot import app
from config.settings import USE_LOCAL_IMAGE_SERVER

# 移除認證設定 (認證檔案已被禁用)

class ServiceManager:
    def __init__(self):
        self.tunnel_process = None
        self.tunnel_url = None
        
        # 獲取端口配置
        try:
            import local_server
            self.port = local_server.port
        except:
            self.port = 8080
    
    def check_cloudflared(self):
        """檢查 cloudflared 是否可用"""
        try:
            result = subprocess.run(['which', 'cloudflared'], capture_output=True)
            return result.returncode == 0
        except:
            return False
    
    def update_dialogflow_webhook(self, url):
        """顯示 Dialogflow webhook URL (需手動設定)"""
        webhook_url = f"{url}/webhook"
        print(f'📝 請手動設定 Dialogflow Webhook: {webhook_url}')
        print(f'🔗 Dialogflow Console: https://dialogflow.cloud.google.com/#/agent/stinkyturtle-ntnj/fulfillment')
        return True
    
    def start_tunnel_async(self):
        """在背景啟動 tunnel"""
        try:
            print(f"🚀 啟動 Cloudflare Tunnel...")
            
            self.tunnel_process = subprocess.Popen(
                ['cloudflared', 'tunnel', '--url', f'http://localhost:{self.port}'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            # 等待並獲取 URL
            start_time = time.time()
            timeout = 30
            
            while time.time() - start_time < timeout:
                line = self.tunnel_process.stdout.readline()
                if line:
                    line = line.strip()
                    
                    # 查找 tunnel URL
                    url_match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
                    if url_match:
                        self.tunnel_url = url_match.group()
                        print(f"🎉 Tunnel URL: {self.tunnel_url}")
                        
                        # 保存 URL 到文件
                        with open('.tunnel_url', 'w') as f:
                            f.write(self.tunnel_url)
                        
                        # 更新 Dialogflow
                        self.update_dialogflow_webhook(self.tunnel_url)
                        
                        print(f"✅ Cloudflare Tunnel 已啟動！")
                        return True
                
                if self.tunnel_process.poll() is not None:
                    print("❌ Cloudflare Tunnel 進程意外退出")
                    break
                    
                time.sleep(0.1)
            
            print("⏰ Tunnel 啟動超時")
            if self.tunnel_process:
                self.tunnel_process.terminate()
            return False
            
        except Exception as e:
            print(f"❌ Tunnel 啟動失敗: {e}")
            return False
    
    def start_services(self):
        """啟動所有服務"""
        print("🐢 StinkyTurtle LINE Bot 啟動中...")
        print("=" * 50)
        
        # 自動決定是否啟動 tunnel
        need_tunnel = USE_LOCAL_IMAGE_SERVER
        can_start_tunnel = self.check_cloudflared()
        
        if need_tunnel and can_start_tunnel:
            print("📡 檢測到需要外部訪問，啟動 Cloudflare Tunnel...")
            
            # 在背景線程啟動 tunnel
            tunnel_thread = threading.Thread(target=self.start_tunnel_async, daemon=True)
            tunnel_thread.start()
            
            # 等待 tunnel 啟動
            time.sleep(3)
            
        elif need_tunnel and not can_start_tunnel:
            print("⚠️  需要外部訪問但 cloudflared 未安裝")
            print("📦 請安裝: brew install cloudflared")
            print("🔄 將以本地模式啟動...")
        
        # 啟動 LINE Bot 服務器
        print("\n" + "=" * 50)
        print(f"🚀 啟動 LINE Bot 服務器在端口 {self.port}")
        print(f"📱 本地 Webhook: http://localhost:{self.port}/webhook")
        
        if self.tunnel_url:
            print(f"🌐 外部 Webhook: {self.tunnel_url}/webhook")
        
        print("⏹️  按 Ctrl+C 停止服務器")
        print("=" * 50)
        
        try:
            uvicorn.run(app, host="0.0.0.0", port=self.port)
        except KeyboardInterrupt:
            self.stop_services()
    
    def stop_services(self):
        """停止所有服務"""
        print("\n🛑 正在停止服務...")
        
        if self.tunnel_process:
            print("🛑 停止 Cloudflare Tunnel...")
            self.tunnel_process.terminate()
            try:
                self.tunnel_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.tunnel_process.kill()
        
        print("👋 服務已停止，再見！")

def main():
    """主函數"""
    service_manager = ServiceManager()
    service_manager.start_services()

if __name__ == "__main__":
    main()