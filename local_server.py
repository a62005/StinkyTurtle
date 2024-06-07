from pyngrok import ngrok

from google.cloud import dialogflow_v2 as dialogflow
from google.protobuf import field_mask_pb2 as field_mask
import os

script_directory = os.path.dirname(os.path.abspath(__file__))
print(script_directory)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f'{script_directory}/dialogflow_auth.json'

def update_dialogflow_callback_url(url):
    client = dialogflow.FulfillmentsClient()

    # 獲取當前Fulfillment
    name = f'projects/stinkyturtle-ntnj/agent/fulfillment'
    fulfillment = client.get_fulfillment(name=name)
    
    # 更新Fulfillment Webhook
    fulfillment.generic_web_service.uri = f"{url}/webhook"

    # 創建FieldMask來指定要更新的字段
    update_mask = field_mask.FieldMask(paths=['generic_web_service.uri', 'generic_web_service.request_headers'])

    # 執行更新請求
    response = client.update_fulfillment(fulfillment=fulfillment, update_mask=update_mask)

    print(f'Updated Fulfillment Webhook: {response}')
    
def run_ngrok(port):
    public_url = ngrok.connect(port).public_url
    print(f" * ngrok tunnel \"{public_url}\" -> \"http://127.0.0.1:{port}\" ")
    update_dialogflow_callback_url(public_url)

# 使用你的端口號來運行ngrok
port = 8001
print(run_ngrok(port))
# list_webhooks()