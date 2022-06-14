from typing import List

from fastapi import APIRouter, Depends, File, Response, status

from app.models import ImageGet, ImageInbox
from app.service.auth import AuthService
from app.service.images import ImagesHandler

router = APIRouter(prefix='/frames', dependencies=[Depends(AuthService.check_token)])


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=List[ImageInbox])
async def load_images(
    files: List[bytes] = File(), handler: ImagesHandler = Depends()
) -> List[ImageInbox]:
    images = handler.load_images(files)
    return images


@router.get(
    '/{frame_id}/', status_code=status.HTTP_200_OK, response_model=List[ImageGet]
)
async def get_images(
    frame_id: int, handler: ImagesHandler = Depends()
) -> List[ImageGet]:
    images = handler.get_images(frame_id)
    return images


@router.delete('/{frame_id}/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_images(frame_id: int, handler: ImagesHandler = Depends()) -> Response:
    handler.delete_images(frame_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
