# # from .app import app
# # from .settings import settings
# # import uvicorn
# #
# # if __name__ == '__main__':
# #     uvicorn.run('app.app:app',
# #     host=settings.server_host,
# #     port=settings.server_port,
# #     reload=True,)
# from io import BytesIO
# from pathlib import Path
# import base64
#
# from .settings import settings
#
# from minio import Minio
# from minio.error import S3Error
#
# IMAGE_PATH = Path('./images/sample_1.jpeg')
#
# client = Minio(
#     endpoint=settings.minio_url,
#     access_key=settings.minio_access_key,
#     secret_key=settings.minio_secret_key,
#     secure=settings.minio_secure,
# )
#
# print(IMAGE_PATH.exists())
#
# found = client.bucket_exists('my-bucket')
# if not found:
#     client.make_bucket('my-bucket')
#
# # if IMAGE_PATH.exists():
# #     with open(IMAGE_PATH, 'rb') as file:
# #         content = BytesIO(file.read())
# #         size = content.getbuffer().nbytes
# #         client.put_object('my-bucket', 'sample_1.jpeg', content, size)
# try:
#     response = client.get_object('my-bucket', 'sample_1.jpeg')
#
#     # print(base64.b64encode(response.read()))
#     content = BytesIO(response.read())
#     print(content)
#     size = content.getbuffer().nbytes
#     print(size)
#     new_response = client.put_object('my-bucket', 'sample_2.jpeg', content, size)
#     result = client.stat_object("my-bucket", "sample_2.jpeg")
#     print(
#         repr(result.last_modified)
#     )
# except S3Error:
#     print("I could not get object!")
#
# # found = client.bucket_exists('my-bucket')
# # content = 'My first content in minio!'
# # content = BytesIO(bytes(content, 'utf-8'))
# # size = content.getbuffer().nbytes
# # if found:
# #     try:
# #         client.remove_bucket('my-bucket')
# #     except S3Error:
# #         print("I could not remove bucket!")
