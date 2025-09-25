import requests
import json
import importlib
import sys
import os

# 處理相對導入問題
try:
    from utils.time_utils import is_time_between, time_until_target, time_until_draft
    from utils.image_utils import async_img_link, get_current_img_link
    from config.settings import RUNNING_TIME, LINE_TOKEN
except ImportError:
    # 如果相對導入失敗，使用絕對導入
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from utils.time_utils import is_time_between, time_until_target, time_until_draft
    from utils.image_utils import async_img_link, get_current_img_link
    from config.settings import RUNNING_TIME, LINE_TOKEN

def handle_ranking_intent(input_text, reply_token, season_is_finished):
    """處理排行榜相關請求"""
    if input_text == '#戰績':
        if season_is_finished:
            return {
                "fulfillmentText": "球季開始了嗎?急什麼"
            }
        if is_time_between('00:00', RUNNING_TIME) and not season_is_finished:
            return {
                "fulfillmentText": f"請於{RUNNING_TIME}後再查詢排行榜"
            }
        
        if season_is_finished:
            link = get_current_img_link()
        else:
            link = async_img_link()
            
        headers = {'Authorization':'Bearer ' + LINE_TOKEN,'Content-Type':'application/json'}
        body = {
            'replyToken': reply_token,
            'messages':[
                {
                    'type': 'text',
                    'text': '【Stinky Turtle League】戰績出來啦'
                }, {
                    'type': 'image',
                    'originalContentUrl': link,
                    'previewImageUrl': link
                }
            ]
        }
        # 使用 requests 方法回傳訊息到 LINE
        result = requests.request('POST', 'https://api.line.me/v2/bot/message/reply',headers=headers,data=json.dumps(body).encode('utf-8'))
        print(f"request {result.text}  {body}")
        
        return {
            "source": "webhookdata"
        }
    else:    
        return {
            "fulfillmentText": " ",
            "source": ""
        }

def handle_bonus_intent(input_text):
    """處理獎金相關請求"""
    if input_text == '#獎金':
        return {
            "source": "webhookdata"
        }
    else:    
        return {
            "fulfillmentText": "資料同步中，兩分鐘後再試",
            "source": ""
        }

def handle_time_intent(input_text):
    """處理時間相關請求"""
    if input_text == '#開季':
        return {
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            f"{time_until_target()}"
                        ]
                    }
                }
            ],
            "source": "webhookdata"
        }
    elif input_text == '#選秀':
        return {
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            f"{time_until_draft()}"
                        ]
                    }
                }
            ],
            "source": "webhookdata"
        }

def handle_name_intent(input_text, req):
    """處理姓名相關請求"""
    if input_text == '#胡哲':
        return {
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            "在那叫什麼"
                        ]
                    }
                }
            ],
            "source": "webhookdata"
        }
    elif '#' in input_text:
        img_url = req['queryResult']['fulfillmentMessages'][0]['image']['imageUri']
        return {
            "fulfillmentMessages": [
                {
                    "image": {
                        "imageUri": img_url
                    }
                }
            ],
            "source": "webhookdata"
        }
    else:    
        return {
            "fulfillmentText": " ",
            "source": ""
        }

def process_webhook_request(req, season_is_finished):
    """處理 webhook 請求的主要邏輯"""
    # 動態重新載入處理器模組，這樣修改後不需要重啟服務器
    import importlib
    import sys
    if 'handlers.webhook_handler' in sys.modules:
        importlib.reload(sys.modules['handlers.webhook_handler'])
    
    input_text = req['queryResult']['queryText']
    intent = req['queryResult']['intent']['displayName']
    reply_token = req['originalDetectIntentRequest']['payload']['data']['replyToken']
    
    if intent == 'Ranking':
        return handle_ranking_intent(input_text, reply_token, season_is_finished)
    elif intent == 'Bonus':
        return handle_bonus_intent(input_text)
    elif intent == 'Time':
        return handle_time_intent(input_text)
    elif intent == 'Name':
        return handle_name_intent(input_text, req)
    
    return {
        "fulfillmentText": "未知的請求",
        "source": ""
    }