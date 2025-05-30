from enum import Enum


class ContentTypeEnum(str, Enum):
    text = "text"
    image = "image"
    video = "video"
    audio = "audio"
