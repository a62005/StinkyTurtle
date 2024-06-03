import sys
sys.path.append('./yfpy/google')
sys.path.append('./yfpy/quickstart')
import sheet
import quickstart
import time
from datetime import datetime, timedelta
import pandas as pd
import dataframe_image as dfi
import requests

def send_notify(token, msg, filepath=None, stickerPackageId=None, stickerId=None):
    payload = {'message': msg}
    headers = {
        "Authorization": "Bearer " + token
     }
    if stickerPackageId and stickerId:
        payload['stickerPackageId'] = stickerPackageId
        payload['stickerId'] = stickerId

    if filepath:
        attachment = {'imageFile': open(filepath, 'rb')}
        print(attachment)
        r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload, files=attachment)
    else:
        print("attachment")
        r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code, r.text

# Test line notify

# 臭烏龜聯賽
token = "Ao7pCGAeIeLluPxy4mQGXv1jhK7tVY29Arc31QuG2Z7"

# 我要發大財
# token = "yrjISonW7S5g5F9xTjuLCs6cpimSdoiIQ8OmiNTaMec"
send_notify(token=token, msg='肥儒真的好帥，水啦', filepath='', stickerPackageId='', stickerId='10856')

