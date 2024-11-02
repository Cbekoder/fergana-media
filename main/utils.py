import json

import requests
from PIL import Image
import os


def resize_image(image_path, output_path, max_size=(1024, 1024)):
    with Image.open(image_path) as img:
        img.thumbnail(max_size)
        img.save(output_path)


def sendArticle(message_id, title, intro, image, categories, region, news_of_the_day):
    bot_token = '7488996758:AAHBX_g4Kb-xKkx1Lmm-Wxv5GpLU_PF9xLA'
    chat_id = '-1002323211510'

    photo_path = os.path.abspath(image)
    resized_photo_path = os.path.abspath('../fergana-media/media/images/resized.png')
    resize_image(photo_path, resized_photo_path)

    caption = (f"{title}\n\n{intro}\n"
                   f"<a href='https://youtube.com'>Batafsil...</a>\n\n"
               f"#{region} {' '.join(f"#{category}" for category in tuple(categories))}")

    inline_keyboard = {
        "inline_keyboard": [
            [
                {
                    "text": "Ko'proq",
                    "url": "https://fergana-media.vercel.app/"  # Replace with your actual link
                }
            ]
        ]
    }
    print(categories)
    payload = {
        'chat_id': chat_id,
        'reply_markup': json.dumps(inline_keyboard)
    }

    if message_id is not None:
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
    else:
        telegram_url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
        payload.update({
            'caption': caption,
            'parse_mode': 'HTML'
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
