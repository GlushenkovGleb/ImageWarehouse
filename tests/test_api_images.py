from pathlib import Path
from unittest.mock import MagicMock

import pytest
from minio import Minio
from urllib3 import HTTPResponse

from app.database import get_minio
from app.models import ImageGet, ImageInbox
from app.tables import Inbox

from .conftest import app


@pytest.mark.parametrize(
    'is_bucket_exists, is_first_image',
    (
        (True, False),
        (False, True),
        (False, True),
    ),
)
def test_load_images(client_test, is_bucket_exists, is_first_image, session):
    # prepare data
    mock_minio = Minio('testing')
    mock_minio.bucket_exists = MagicMock(return_value=is_bucket_exists)
    mock_minio.make_bucket = MagicMock(return_value=None)
    mock_minio.put_object = MagicMock(return_value=None)

    def my_get_minio() -> Minio:
        return mock_minio

    # check that it works fine without images in db
    if is_first_image:
        image = session.query(Inbox).filter(Inbox.id == 1).first()
        session.delete(image)
        session.commit()

    app.dependency_overrides[get_minio] = my_get_minio

    # testing
    file_name = Path('./tests/data/sample_1.jpeg')
    with open(file_name, 'rb') as file:
        response = client_test.post(
            '/frames/', files={'files': ('filename', file, 'image/jpeg')}
        )
        assert response.status_code == 201
        assert list(map(ImageInbox.parse_obj, response.json()))
        mock_minio.bucket_exists.assert_called_once()
        mock_minio.put_object.assert_called_once()
        if is_bucket_exists:
            mock_minio.make_bucket.assert_not_called()
        else:
            mock_minio.make_bucket.assert_called_once()


def test_get_images(client_test):
    # prepare
    file_name = Path('./tests/data/sample_1.jpeg')
    with open(file_name, 'rb') as file:
        content = file.read()

    # create mocks
    mock_response = HTTPResponse()
    mock_response.read = MagicMock(return_value=content)
    mock_minio = Minio('testing')
    mock_minio.get_object = MagicMock(return_value=mock_response)

    def my_minio() -> Minio:
        return mock_minio

    app.dependency_overrides[get_minio] = my_minio

    # testing
    response = client_test.get('/frames/1')
    assert response.status_code == 200
    assert list(map(ImageGet.parse_obj, response.json()))
    mock_minio.get_object.assert_called_once()


def test_delete_images(client_test, session):
    # prepare
    mock_minio = Minio('testing')
    mock_minio.remove_object = MagicMock(return_value=None)

    def my_minio() -> Minio:
        return mock_minio

    app.dependency_overrides[get_minio] = my_minio

    # testing
    response = client_test.delete('/frames/1')
    assert response.status_code == 204
    mock_minio.remove_object.assert_called_once()

    # check db
    image = session.query(Inbox).filter(Inbox.frame_id == 1).first()
    assert image is None
