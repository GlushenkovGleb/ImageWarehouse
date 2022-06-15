import base64
import uuid
from datetime import datetime
from io import BytesIO
from typing import Any, List, Tuple

from fastapi import Depends
from minio import Minio
from sqlalchemy.orm import Session
from urllib3 import HTTPResponse

from app import models
from app.database import get_minio, get_session
from app.tables import Inbox


class ImagesHandler:
    """Class that handles images using minio and sql"""
    @staticmethod
    def gen_image_name() -> str:
        return f'{uuid.uuid4()}.jpg'

    @staticmethod
    def get_bucket_name(date: datetime) -> str:
        return date.strftime('%Y%m%d')

    @staticmethod
    def get_file_content(data: bytes) -> Tuple[Any, int]:
        raw_data = BytesIO(data)
        size = raw_data.getbuffer().nbytes
        return raw_data, size

    @staticmethod
    def encode_image(file: HTTPResponse) -> bytes:
        return base64.b64encode(file.read())

    def __init__(
        self,
        session: Session = Depends(get_session),
        minio_client: Minio = Depends(get_minio),
    ):
        self.session = session
        self.minio_client = minio_client

    def load_images(self, files: List[bytes]) -> List[models.ImageInbox]:
        """Load images in db and buckets using minio"""
        # get last request id
        lst_frame_id = (
            self.session.query(Inbox.frame_id).order_by(Inbox.id.desc()).first()
        )
        if lst_frame_id is None:
            lst_frame_id = 0
        else:
            (lst_frame_id,) = lst_frame_id
        frame_id = lst_frame_id + 1

        inbox_list = [
            Inbox(name=self.gen_image_name(), frame_id=frame_id)
            for _ in range(len(files))
        ]
        self.session.add_all(inbox_list)
        self.session.flush()

        # put images in bucket
        for image, file in zip(inbox_list, files):
            bucket_name = self.get_bucket_name(image.created_at)
            if not self.minio_client.bucket_exists(bucket_name):
                self.minio_client.make_bucket(bucket_name)

            raw_content, size = self.get_file_content(file)
            self.minio_client.put_object(bucket_name, image.name, raw_content, size)

        self.session.commit()
        return list(map(models.ImageInbox.from_orm, inbox_list))

    def get_images(self, frame_id: int) -> List[models.ImageGet]:
        """Gets images from minio and db, and returns content of image encoded in base64"""
        inbox_list = self.session.query(Inbox).filter(Inbox.frame_id == frame_id).all()
        images = []
        for image in inbox_list:
            bucket_name = self.get_bucket_name(image.created_at)
            file = self.minio_client.get_object(bucket_name, image.name)
            content = self.encode_image(file)
            inbox_model = models.ImageInbox.from_orm(image)
            images.append(models.ImageGet(**inbox_model.dict(), content=content))
        return images

    def delete_images(self, frame_id: int) -> None:
        """Deletes images from minio and db"""
        inbox_list = self.session.query(Inbox).filter(Inbox.frame_id == frame_id).all()
        for image in inbox_list:
            bucket_name = self.get_bucket_name(image.created_at)
            self.minio_client.remove_object(bucket_name, image.name)
        for image in inbox_list:
            self.session.delete(image)
        self.session.commit()
