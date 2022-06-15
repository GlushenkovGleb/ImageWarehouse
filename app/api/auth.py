from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.models import Token, UserCreate
from app.service.auth import AuthService

router = APIRouter(prefix='/auth')


@router.post('/sign-up/', status_code=status.HTTP_201_CREATED, response_model=Token)
async def sign_up(user_data: UserCreate, service: AuthService = Depends()) -> Token:
    return service.register_new_user(user_data)


@router.post('/sign-in/', status_code=status.HTTP_201_CREATED, response_model=Token)
async def sing_up(
    form_data: OAuth2PasswordRequestForm = Depends(), service: AuthService = Depends()
) -> Token:
    return service.authenticate_user(form_data.username, form_data.password)
