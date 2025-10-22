from fastapi.responses import Response
import os
import sys

# 處理相對導入問題
try:
    from config.settings import USE_LOCAL_IMAGE_SERVER
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from config.settings import USE_LOCAL_IMAGE_SERVER

def setup_image_routes(app):
    """設置圖片服務路由"""
    
    @app.get("/image/current")
    def get_current_image():
        """提供當前的戰績圖片"""
        script_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        img_path = f"{script_directory}/dataframe_image.png"
        
        if os.path.exists(img_path):
            with open(img_path, "rb") as f:
                image_data = f.read()
            return Response(
                content=image_data,
                media_type="image/png",
                headers={
                    "Cache-Control": "no-cache",
                    "Content-Disposition": "inline"
                }
            )
        else:
            return {"error": "Image not found"}

    @app.get("/image/test")
    def get_test_image():
        """提供測試圖片"""
        script_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        img_path = f"{script_directory}/test.jpg"
        
        if os.path.exists(img_path):
            with open(img_path, "rb") as f:
                image_data = f.read()
            return Response(
                content=image_data,
                media_type="image/jpeg",
                headers={
                    "Cache-Control": "no-cache",
                    "Content-Disposition": "inline"
                }
            )
        else:
            return {"error": "Test image not found"}

def get_server_url():
    """獲取服務器 URL"""
    # 1. 從環境變量獲取
    tunnel_url = os.getenv('CLOUDFLARE_TUNNEL_URL')
    if tunnel_url:
        return tunnel_url
    
    # 2. 從 .tunnel_url 文件獲取（僅在非 App Engine 環境）
    if not os.environ.get('GAE_ENV', '').startswith('standard'):
        try:
            script_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            tunnel_file = os.path.join(script_directory, '.tunnel_url')
            if os.path.exists(tunnel_file):
                with open(tunnel_file, 'r') as f:
                    url = f.read().strip()
                    if url:
                        return url
        except:
            pass
    
    # 3. 從 .env 文件獲取
    try:
        script_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        env_file = os.path.join(script_directory, '.env')
        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                for line in f:
                    if line.startswith('CLOUDFLARE_TUNNEL_URL='):
                        return line.split('=', 1)[1].strip()
    except:
        pass
    
    print("⚠️  未找到 Cloudflare Tunnel URL")
    print("💡 請先啟動 tunnel: python start_tunnel.py")
    return "http://localhost:8001"  # 備用 URL

def get_test_image_url():
    """獲取測試圖片 URL"""
    if USE_LOCAL_IMAGE_SERVER:
        server_url = get_server_url()
        return f"{server_url}/image/test"
    else:
        return None