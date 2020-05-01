from fastapi import APIRouter

router = APIRouter()


@router('/send_email', tags=['email'])
def send_email():
    return
