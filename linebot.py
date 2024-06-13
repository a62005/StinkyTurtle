import uvicorn
import requests
import json
from fastapi import FastAPI, Request
from datetime import datetime
import pyimgur
import os
import schedule
import time
import threading
import print_data

app = FastAPI()
script_directory = os.path.dirname(os.path.abspath(__file__))
im = pyimgur.Imgur("22cca6882f4dfe8")

def checkDate(date: str) -> bool:
    if not date:
        return False
    # 獲取當前日期並將其格式化為字符串
    current_date = datetime.now().strftime('%Y-%m-%d')
    # 將輸入的日期與當前日期進行比較
    return date == current_date

running_tiem = '14:00'
start_time = datetime.strptime('00:00', '%H:%M').time()
end_time = datetime.strptime(running_tiem, '%H:%M').time()

def is_time_between():
    # 如果開始時間小於結束時間，則檢查當前時間是否在這個範圍內 
    if start_time < end_time:
        return start_time <= datetime.now().time() <= end_time
    # 如果開始時間大於結束時間，則檢查當前時間是否在這個範圍內
    else:
        return datetime.now().time() >= start_time or datetime.now().time() <= end_time

def asyncImgLink():
    img = f"{script_directory}/dataframe_image.png"
    with open(f"{script_directory}/config/img_data.json", 'r', encoding='utf-8') as r:
        imgData = json.load(r)
    date = imgData['date']
    if checkDate(date):
        link = imgData['imgurl']
    else:
        print_data.main()
        uploaded_img = im.upload_image(img, title="Test by Turtle")
        link = uploaded_img.link
        imgData['date'] = datetime.now().strftime('%Y-%m-%d')
        imgData['imgurl'] = link
        # 再以寫入模式打開文件，寫入數據
        with open(f"{script_directory}/config/img_data.json", 'w', encoding='utf-8') as w:
            json.dump(imgData, w)
    return link

def job():
    print_data.main()

def run_schedule():
    schedule.every().day.at("13:55").do(job)
    
    while True:
        print("Running...")
        schedule.run_pending()
        time.sleep(300)

schedule_thread = threading.Thread(target=run_schedule)
schedule_thread.daemon = True  # 設置為守護線程，使其在主程序退出時自動終止
schedule_thread.start()

import local_server

@app.get("/")
def home():
    return "hello world"

@app.post('/webhook')
async def webhook(request: Request):
    req = await request.json()
    print(req)
    inputText = req['queryResult']['queryText']              # 取得使用者輸入文字
    reText = req['queryResult']['fulfillmentText']          # 取得 Dialogflow 的回應文字
    intent = req['queryResult']['intent']['displayName']    # 取得 intent 分類
    replytoken = req['originalDetectIntentRequest']['payload']['data']['replyToken']  # 取得 LINE replyToken
    token = 'QwDA02XsTA0E1gostK0dmOjPSevU7NlD1jAWqIdegEkW+oKhpO005GPoT+ReeCHv4Hno33b1FQie+prDNWBklzi3YL0e/pep+U+7IG5jubfuVuT4RtFt0PDtgkfZr2i5XC+kv4ZXBQcmeszYnG3iZQdB04t89/1O/w1cDnyilFU='
    
    if intent=='Ranking':
        if inputText == '#戰績':
            if is_time_between():
                return {
                    "fulfillmentText": f"請於{running_tiem}後再查詢排行榜"
                }
            link = asyncImgLink()
            headers = {'Authorization':'Bearer ' + token,'Content-Type':'application/json'}
            body = {
                'replyToken':replytoken,
                'messages':[
                    {
                    'type': 'text',
                    'text': '【Stinky Turtle League】戰績出來啦'
                    },{
                        'type': 'image',
                        'originalContentUrl': link,
                        'previewImageUrl': link
                    }
                ]
            }
            # 使用 requests 方法回傳訊息到 ＬINE
            result = requests.request('POST', 'https://api.line.me/v2/bot/message/reply',headers=headers,data=json.dumps(body).encode('utf-8'))
            print(f"request {result.text}  {body}")
            # 完成後回傳訊息到 Dialogflow
        else:    
            return {
                "fulfillmentText": " ",
                "source": ""
            }
        return {
            "source": "webhookdata"
        }
    # 如果收到的 intent 不是 radar
    else:
        # 使用 Dialogflow 產生的回應訊息
        return {
            "fulfillmentText": f'{reText} ( webhook )'
        }
uvicorn.run(app, port=local_server.port)