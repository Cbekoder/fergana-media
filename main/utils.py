import json

import requests
from PIL import Image
import os

bot_token = '7488996758:AAHBX_g4Kb-xKkx1Lmm-Wxv5GpLU_PF9xLA'
chat_id = '-1002323211510'


def resize_image(image_path, output_path, max_size=(1024, 1024)):
    with Image.open(image_path) as img:
        img.thumbnail(max_size)
        img.save(output_path)


def sendArticle(id, message_id, title, intro, image, categories, region, news_of_the_day):
    photo_path = os.path.abspath(image)
    resized_photo_path = os.path.abspath('resized.png')
    resize_image(photo_path, resized_photo_path)

    caption = f"""{title}\n\n{intro}\n
<a href='https://fergana-media.vercel.app/news/{id}/?type=world'>Batafsil...</a>\n\n
{f"#{region} " if region else ""}{' '.join(f"#{category}" for category in tuple(categories))}\n\n@ferganamedia"""

    payload = {
        'chat_id': chat_id,
    }

    if message_id is None:
        telegram_url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
        payload.update({
            'caption': caption,
            'parse_mode': 'HTML'
        })
    else:
        telegram_url = f"https://api.telegram.org/bot{bot_token}/editMessageMedia"
        new_image = {
            "type": "photo",
            "media": "attach://photo",
            "caption": caption,
            "parse_mode": "HTML"
        }
        payload.update({
            'message_id': message_id,
            "media": json.dumps(new_image)
        })


    with open(resized_photo_path, 'rb') as photo:
        files = {
            "photo": photo
        }
        response = requests.post(telegram_url, data=payload, files=files)

    if os.path.exists(resized_photo_path):
        os.remove(resized_photo_path)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to send photo. Error: {response.status_code} - {response.text}")

def sendVideo(message_id, title, intro, cover, url, categories):
    caption = f"""{title}\n\n{intro}\n
<a href='{url}'>To'liq video</a>\n\n
{' '.join(f"#{category}" for category in tuple(categories))}\n\n@ferganamedia"""

    payload = {
        'chat_id': chat_id,
        "parse_mode": "HTML"
    }
    if cover:
        photo_path = os.path.abspath(cover)
        resized_photo_path = os.path.abspath('resized.png')
        resize_image(photo_path, resized_photo_path)

        if message_id is None:
            telegram_url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
            payload.update({
                'caption': caption,
                'parse_mode': 'HTML'
            })
        else:
            telegram_url = f"https://api.telegram.org/bot{bot_token}/editMessageMedia"
            new_image = {
                "type": "photo",
                "media": "attach://photo",
                "caption": caption,
                "parse_mode": "HTML"
            }
            payload.update({
                'message_id': message_id,
                "media": json.dumps(new_image)
            })


        with open(resized_photo_path, 'rb') as photo:
            files = {
                "photo": photo
            }
            response = requests.post(telegram_url, data=payload, files=files)

        if os.path.exists(resized_photo_path):
            os.remove(resized_photo_path)
    else:
        if message_id is None:
            telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            data = {
                "chat_id": chat_id,
                "text": caption,
                "parse_mode": "HTML"
            }
        else:
            telegram_url = f"https://api.telegram.org/bot{bot_token}/editMessageText"
            data = {
                "chat_id": chat_id,
                "message_id": message_id,
                "text": caption,
                "parse_mode": "HTML"
            }
        response = requests.post(telegram_url, data=data)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to send photo. Error: {response.status_code} - {response.text}")


def delete_message(message_id):
    telegram_url = f"https://api.telegram.org/bot{bot_token}/deleteMessage"
    data = {
        "chat_id": chat_id,
        "message_id": message_id
    }
    response = requests.post(telegram_url, data=data)
    if response.status_code == 200:
        return {'status': 200, 'detail': "Message deleted successfully!"}
    else:
        return {'status': response.status_code, 'detail': response.text}
