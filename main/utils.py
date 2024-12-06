import json
import requests
from PIL import Image
import os
import bleach
from .models import Credentials
from uuid import uuid4

def custom_filename_generator(filename, request):
    extension = filename.split('.')[-1]
    return f"{uuid4()}.{extension}"

def sanitize_for_telegram(content):
    allowed_tags = ['b', 'i', 'u', 's', 'a', 'code', 'pre']
    return bleach.clean(content, tags=allowed_tags, strip=True)

def resize_image(image_path, output_path, max_size=(1024, 1024)):
    with Image.open(image_path) as img:
        img.thumbnail(max_size)
        img.save(output_path)


def sendArticle(id, message_id, title, intro, image):
    credentials = Credentials.objects.last()
    if credentials:
        bot_token = credentials.botToken
        chat_id = credentials.channel_id
        domain = credentials.domain
        tgChannel = credentials.telegram

    photo_path = os.path.abspath(image)
    resized_photo_path = os.path.abspath('resized.png')
    resize_image(photo_path, resized_photo_path)
    sanitized_content = sanitize_for_telegram(intro)

    caption = f"""{title}\n\n{sanitized_content}...
<a href='https://{domain}/news/{id}/?type=world'>Batafsil...</a>\n
{tgChannel}"""

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

def sendVideo(id, message_id, title, intro, cover, url, video):
    credentials = Credentials.objects.last()
    if credentials:
        bot_token = credentials.botToken
        chat_id = credentials.channel_id
        domain = credentials.domain
        tgChannel = credentials.telegram

    sanitized_content = sanitize_for_telegram(intro)

    caption = f"""{title}\n\n{sanitized_content}
<a href='https://{domain}/news/{id}/?type=world'>Batafsil...</a>\n
"""
    if url:
        caption += f"<a href='{url}'>Video...</a>\n\n{tgChannel}"

    payload = {
        'chat_id': chat_id,
    }
    if video:
        if message_id is None:
            telegram_url = f"https://api.telegram.org/bot{bot_token}/sendVideo"
            payload.update({
                'caption': caption,
                "parse_mode": "HTML"
            })
            with open(video, 'rb') as video_file:
                files = {
                    "video": video_file
                }
                response = requests.post(telegram_url, data=payload, files=files)
        else:
            telegram_url = f"https://api.telegram.org/bot{bot_token}/editMessageMedia"
            new_video = {
                "type": "video",
                "media": "attach://video",
                "caption": caption,
                "parse_mode": "HTML"
            }
            payload.update({
                'message_id': message_id,
                'media': json.dumps(new_video)
            })
            with open(video, 'rb') as video_file:
                files = {
                    "video": video_file
                }
                response = requests.post(telegram_url, data=payload, files=files)
    elif cover:
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
    credentials = Credentials.objects.last()
    if credentials:
        bot_token = credentials.botToken
        chat_id = credentials.channel_id
        domain = credentials.domain
        tgChannel = credentials.telegram

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
