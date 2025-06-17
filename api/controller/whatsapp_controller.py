from fastapi.responses import JSONResponse
import requests
from api.exceptions.message import GenericError
from fastapi import APIRouter, HTTPException, Query, Depends
from api.models.enums.type import ContentTypeEnum
import os

from api.core.jwt_bearer import JwtBearer

router = APIRouter(prefix="/whats", tags=["Whatsapp"])


@router.post(
    "/sendMessage",
    response_model=GenericError,
    responses={
        201: {"model": GenericError, "description": "Mensagem Enviada!!!"},
        400: {
            "model": GenericError,
            "description": "Não foi possivel enviar a mensagem",
        },
        404: {
            "model": GenericError,
            "description": "Número ou Instancia não encotrada",
        },
        500: {
            "model": GenericError,
            "description": "Problema com o Acesso ao API do Whatsapp",
        },
    },
    status_code=201,
    dependencies=[Depends(JwtBearer())],
)
def send_message(number: str, message: str):
    response = requests.post(
        os.getenv("WEBHOOK_WHATS_SEND_MESSAGE"),
        json={"number": number, "message": message},
    )

    if response.status_code != 201:
        raise HTTPException(
            status_code=response.status_code, detail="Falha ao enviar a mensagem"
        )

    return JSONResponse(status_code=201, content="Mensagem Enviada")


@router.post(
    "/sendMedia",
    response_model=GenericError,
    responses={
        201: {"model": GenericError, "description": "Media Enviada!!!"},
        400: {"model": GenericError, "description": "Não foi possivel Enviar a Media"},
        404: {
            "model": GenericError,
            "description": "Número ou Instancia não encotrada",
        },
        500: {
            "model": GenericError,
            "description": "Problema com o Acesso ao API do Whatsapp",
        },
    },
    status_code=201,
    dependencies=[Depends(JwtBearer())],
)
def send_media(
    number: str,
    media_url: str,
    caption: str,
    type_media: ContentTypeEnum = Query(default=ContentTypeEnum.image),
):
    response = requests.post(
        os.getenv("WEBHOOK_WHATS_SEND_MEDIA"),
        json={
            "number": number,
            "media_url": media_url,
            "caption": caption,
            "type": type_media,
        },
    )
    if response.status_code != 201:
        raise HTTPException(
            status_code=response.status_code, detail="Falha ao enviar Media"
        )

    return JSONResponse(status_code=201, content="Media Enviado!")


@router.post(
    "/send_audio",
    response_model=GenericError,
    responses={
        201: {"model": GenericError, "description": "Audio Enviado!!!"},
        400: {"model": GenericError, "description": "Não foi possivel enviar o Audio"},
        404: {
            "model": GenericError,
            "description": "Número ou Instancia não encotrada",
        },
        500: {
            "model": GenericError,
            "description": "Problema com o Acesso ao API do Whatsapp",
        },
    },
    status_code=201,
    dependencies=[Depends(JwtBearer())],
)
def send_audio(number: str, audio_url: str):
    response = requests.post(
        os.getenv("WEBHOOK_WHATS_SEND_AUDIO"),
        json={"number": number, "audio_url": audio_url},
    )

    if response.status_code != 201:
        raise HTTPException(
            status_code=response.status_code, detail="Falha ao enviar audio"
        )

    return JSONResponse(status_code=201, content="Audio Enviado")

