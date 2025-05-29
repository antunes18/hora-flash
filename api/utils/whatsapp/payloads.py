# DEFAULT
payload_default = {
    "number": "<string>",
    "options": {"delay": 123, "presence": "composing"},
}


# PAYLOAD DE ENVIO

# PLAIN TEXT
payload_send_plain_text = dict(payload_default)

### OPTIONAL

options = {
    "delay": 123,
    "presence": "composing",
    "linkPreview": True,
    "quoted": {
        "key": {
            "remoteJid": "",
            "fromMe": True,
            "id": "",
            "participant": "",
        },
        "message": {"conversation": ""},
    },
    "metions": {"everyOne": True, "mentioned": [""]},
}


### SEND_MEDIAS
payload_send_plain_text["options"] = dict(options)

payload_media = dict(payload_default)

payload_media.update(
    {
        "mediaMessage": {
            "mediaType": "image",
            "fileName": "",
            "caption": "",
            "media": "",
        },
        "mediatype": "image",
    }
)


### SEND_STATUS
payload_send_status = dict(payload_default)

payload_send_status.update(
    {
        "type": "image",
        "content": "https://s2-techtudo.glbimg.com/Yy8GvFtkaN6KNguiLm-dkTbLnWg=/0x0:1280x720/984x0/smart/filters:strip_icc()/i.s3.glbimg.com/v1/AUTH_08fbf48bc0524877943fe86e43087e7a/internal_photos/bs/2021/C/h/u09RKXTxAUwTFATXhElA/the-russo-bros-directed-fortnite-season-6s-cinematic-and-killed-peely-again-feature.jpg",
        "caption": "",
        "backgroudColor": "",
        "font": 5,
        "allContacts": True,
        "statusJidList": [""],
    }
)


### SEND AUDIO
payload_audio = dict(payload_default)

payload_audio.update({"audio": ""})


### SEND STICKER

payload_sticker = dict(payload_default)
# payload_sticker.update({"image": ""})


### FAKE CALL
payload_call = {"number": "", "isVideo": False, "callDuration": 3}

if __name__ == "__main__":
    print(payload_media)
