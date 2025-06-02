from fastapi.responses import JSONResponse
from api.execptions.message import GenericError
from api.utils.whatsapp import methods
from fastapi import APIRouter, HTTPException, Query
from api.models.enums.type import ContentTypeEnum


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
)
def send_message(number: str, text: str):
    response = methods.send_message(number, text)

    if response.status_code != 201:
        raise HTTPException(
            status_code=response.status_code, detail="Falha ao enviar a mensagem"
        )

    return JSONResponse(status_code=201, content="GenericError Enviada")


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
)
def send_media(
    number: str,
    media_url: str,
    caption: str,
):
    response = methods.send_media(number, media_url=media_url, caption=caption)
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
)
def send_audio(number: str, audio_url: str):
    response = methods.send_audio(number, audio_url)

    if response.status_code != 201:
        raise HTTPException(
            status_code=response.status_code, detail="Falha ao enviar audio"
        )

    return JSONResponse(status_code=201, content="Audio Enviado")


@router.post(
    "/send_status",
    response_model=GenericError,
    responses={
        201: {"model": GenericError, "description": "Status Enviado com Sucesso!!!"},
        400: {"model": GenericError, "description": "Não foi possivel enviar o Status"},
        404: {
            "model": GenericError,
            "description": "Número ou Instancia não encotrada",
        },
        500: {
            "model": GenericError,
            "description": "Problema com o Acesso ao API do Whatsapp",
        },
    },
)
def send_status(
    content: str,
    type: ContentTypeEnum = Query(default=ContentTypeEnum.text),
):
    response = methods.send_status(type=type, backgroundColor="red", content=content)

    if response.status_code != 201:
        raise HTTPException(
            status_code=response.status_code, detail="Falha ao enviar Status"
        )

    return JSONResponse(status_code=201, content="Status Enviado")


@router.post(
    "/send_sticker",
    response_model=GenericError,
    responses={
        201: {"model": GenericError, "description": "Sticker Enviada!!!"},
        400: {
            "model": GenericError,
            "description": "Não foi possivel enviar o Sticker",
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
)
def send_sticker(number: str, image_url: str):
    response = methods.send_sticker(number, image_url)

    if response.status_code != 201:
        raise HTTPException(
            status_code=response.status_code, detail="Falha ao enviar Sticker"
        )

    return JSONResponse(status_code=201, content="Sticker Enviado")
