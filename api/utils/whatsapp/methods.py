import os
from dotenv import load_dotenv
from fastapi import responses
import requests

from api.utils.whatsapp import payloads

load_dotenv()

instance = os.getenv("USER_INSTANCE")
API_URL = os.getenv("API_URL")
headers = {"apikey": os.getenv("API_KEY"), "Content-Type": "application/json"}
url_send_plain_text = f"{API_URL}/message/sendText/{instance}"
url_send_media = f"{API_URL}/message/sendMedia/{instance}"
url_send_status = f"{API_URL}/message/sendStatus/{instance}"
url_send_audio = f"{API_URL}/message/sendWhatsAppAudio/{instance}"
url_send_sticker = f"{API_URL}/message/sendSticker/{instance}"
url_send_location = f"{API_URL}/message/sendLocation/{instance}"

url_fake_call = f"{API_URL}/call/offer/{instance}"


def send_message(number: str, text: str):
    if not number or not text:
        raise ValueError("Number or Text Not Informed!!!")
    payload = dict(payloads.payload_send_plain_text)
    payload.update({"number": number})
    payload["text"] = text

    return requests.post(url_send_plain_text, json=payload, headers=headers)


def send_media(number: str, media_url: str, caption: str):
    mediatype: str = "image"

    if not number:
        raise ValueError("Number Not Informed!!!")

    if media_url.endswith(".mp3"):
        mediatype = "audio"

    if media_url.endswith(".mp4"):
        mediatype = "video"

    payload = dict(payloads.payload_media)
    payload.update({"number": number})
    payload.update(
        {
            "mediatype": mediatype,
            "media": media_url,
            "caption": caption,
        }
    )
    return requests.post(url_send_media, json=payload, headers=headers)


def send_status(content: str, backgroundColor: str, type: str = "text"):
    payload = dict(payloads.payload_send_status)
    payload.update(
        {
            "content": content,
            "backgroundColor": backgroundColor,
            "statusJidList": ["0000000000@s.whatsapp.net"],
            "type": type,
        }
    )
    return requests.post(url_send_status, json=payload, headers=headers)


def send_audio(number: str, audio_url: str):
    if not number:
        raise ValueError("Number Not Informed!!!")

    payload = payloads.payload_audio
    payload.update({"number": number})
    payload.update({"audio": audio_url})

    return requests.post(url_send_audio, json=payload, headers=headers)


def send_sticker(number: str, image_url):
    if not number:
        raise ValueError("Number Not Informed!!!")

    payload = dict(payloads.payload_sticker)

    payload.update({"number": number, "sticker": image_url})

    return requests.post(url_send_sticker, json=payload, headers=headers)


def fake_call(number: str):
    if not number:
        raise ValueError("Number Not Informed!!!")

    payload = payloads.payload_call
    payload.update({"number": number, "isVideo": False, "callDuration": 3})

    return requests.post(url_fake_call, json=payload, headers=headers)


def send_location(number: str, address: str, longitude: int, latitude: int):
    payload = dict(payloads.payload_location)

    payload.update(
        {
            "number": number,
            "name": "Casa da Sua Mãe",
            "address": address,
            "longitude": longitude,
            "latitude": latitude,
        }
    )

    return requests.post(url_send_location, json=payload, headers=headers)


if __name__ == "__main__":
    pass
    # send_image(number="00 0000 0000"", image_url="https://s2-techtudo.glbimg.com/Yy8GvFtkaN6KNguiLm-dkTbLnWg=/0x0:1280x720/984x0/smart/filters:strip_icc()/i.s3.glbimg.com/v1/AUTH_08fbf48bc0524877943fe86e43087e7a/internal_photos/bs/2021/C/h/u09RKXTxAUwTFATXhElA/the-russo-bros-directed-fortnite-season-6s-cinematic-and-killed-peely-again-feature.jpg",caption="teste de image")
    # send_status("https://s2-techtudo.glbimg.com/Yy8GvFtkaN6KNguiLm-dkTbLnWg=/0x0:1280x720/984x0/smart/filters:strip_icc()/i.s3.glbimg.com/v1/AUTH_08fbf48bc0524877943fe86e43087e7a/internal_photos/bs/2021/C/h/u09RKXTxAUwTFATXhElA/the-russo-bros-directed-fortnite-season-6s-cinematic-and-killed-peely-again-feature.jpg","Red","image")
    # send_audio("00 0000 0000"", "https://www.myinstants.com/media/sounds/inutilismo-mas-que-merda.mp3",)
    # send_sticker("00 0000 0000", "https://m.media-amazon.com/images/I/61nWmtoLUcL._SY466_.jpg")
