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
        "content": "",
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


### SEND LOCATION

payload_location = dict(payload_default)
payload_location.update(
    {
        "number": "",
        "name": "",
        "address": "",
        "latitude": -16.505538233564373,
        "longitude": -151.7422770494996,
    }
)


### FAKE CALL
payload_call = {"number": "", "isVideo": False, "callDuration": 3}

if __name__ == "__main__":
    print(payload_media)
