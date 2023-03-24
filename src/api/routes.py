from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException


router = APIRouter()


@router.get("/", status_code=HTTPStatus.OK)
async def root():
    return {"message": "Hello Bro"}
