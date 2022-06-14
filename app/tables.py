import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()  # type: ignore


class Inbox(Base):  # type: ignore
    __tablename__ = 'inbox'

    id = sa.Column(sa.Integer, primary_key=True)
    frame_id = sa.Column(sa.Integer, nullable=False)
    name = sa.Column(sa.String, nullable=False)
    created_at = sa.Column(
        sa.types.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
    )


class User(Base):  # type: ignore
    __tablename__ = 'user'

    id = sa.Column(sa.Integer, primary_key=True)
    login = sa.Column(sa.String, unique=True, nullable=False)
    password_hash = sa.Column(sa.String)

    def __repr__(self):
        return f'User(id={self.id}, login={self.login}, password_hash={self.password_hash})'
