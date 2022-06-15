from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models
from app.database import get_session
from app.settings import settings
from app.tables import User


class AuthService:
    pwd_contex = CryptContext(schemes=['bcrypt'], deprecated='auto')
    oath2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/sign-in/')

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls.pwd_contex.verify(plain_password, hashed_password)

    @classmethod
    def get_hashed_password(cls, password: str) -> str:
        return cls.pwd_contex.hash(password)

    @classmethod
    def validate_token(cls, token: str) -> None:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )

        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret_key,
                algorithms=[settings.jwt_algorithm],
            )
        except JWTError:
            raise credentials_exception from None

        user_data = payload.get('user')
        try:
            models.User.parse_obj(user_data)
        except ValidationError:
            raise credentials_exception from None

    @classmethod
    def create_token(cls, user: User) -> models.Token:
        user_data = models.User.from_orm(user)

        now = datetime.utcnow()
        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(minutes=settings.jwt_expire_minutes),
            'sub': str(user_data.id),
            'user': user_data.dict(),
        }
        token = jwt.encode(
            payload,
            settings.jwt_secret_key,
            algorithm=settings.jwt_algorithm,
        )

        return models.Token(access_token=token)

    @classmethod
    def check_token(cls, token: str = Depends(oath2_scheme)) -> None:
        return cls.validate_token(token)

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def register_new_user(self, user_data: models.UserCreate) -> models.Token:
        user = User(
            login=user_data.login,
            password_hash=self.get_hashed_password(user_data.password),
        )
        try:
            self.session.add(user)
            self.session.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='User with this login already exists',
            ) from None

        return self.create_token(user)

    def authenticate_user(self, login: str, password: str) -> models.Token:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

        user = self.session.query(User).filter(User.login == login).first()

        if user is None:
            raise credentials_exception

        if not self.verify_password(password, user.password_hash):
            raise credentials_exception

        return self.create_token(user)
