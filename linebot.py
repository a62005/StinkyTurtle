import uvicorn
import requests
import json
from fastapi import FastAPI, Request
import pyimgur

app = FastAPI()
import os

script_directory = os.path.dirname(os.path.abspath(__file__))
im = pyimgur.Imgur("22cca6882f4dfe8")


@app.get("/")
def home():
    return "hello world"

@app.post('/webhook')
async def webhook(request: Request):
    req = await request.json()
    print(req)
    reText = req['queryResult']['fulfillmentText']          # 取得 Dialogflow 的回應文字
    intent = req['queryResult']['intent']['displayName']    # 取得 intent 分類
    replytoken = req['originalDetectIntentRequest']['payload']['data']['replyToken']  # 取得 LINE replyToken
    token = 'QwDA02XsTA0E1gostK0dmOjPSevU7NlD1jAWqIdegEkW+oKhpO005GPoT+ReeCHv4Hno33b1FQie+prDNWBklzi3YL0e/pep+U+7IG5jubfuVuT4RtFt0PDtgkfZr2i5XC+kv4ZXBQcmeszYnG3iZQdB04t89/1O/w1cDnyilFU='
   
    img = f"{script_directory}/dataframe_image.png"
    
    if intent=='Ranking':
        uploaded_img = im.upload_image(img, title="Test by Turtle")
        headers = {'Authorization':'Bearer ' + token,'Content-Type':'application/json'}
        body = {
            'replyToken':replytoken,
            'messages':[{
                    'type': 'image',
                    'originalContentUrl': uploaded_img.link,
                    'previewImageUrl': uploaded_img.link
                }]
            }
        # 使用 requests 方法回傳訊息到 ＬINE
        result = requests.request('POST', 'https://api.line.me/v2/bot/message/reply',headers=headers,data=json.dumps(body).encode('utf-8'))
        print(f"request {result.text}  {body}")
        # 完成後回傳訊息到 Dialogflow
        return {
            "source": "webhookdata"
        }
    # 如果收到的 intent 不是 radar
    else:
        # 使用 Dialogflow 產生的回應訊息
        return {
            "fulfillmentText": f'{reText} ( webhook )'
        }
uvicorn.run(app, port=8001)