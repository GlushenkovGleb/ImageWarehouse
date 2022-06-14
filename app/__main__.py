import uvicorn

from .database import init_db
from .settings import settings

if __name__ == '__main__':
    init_db()
    uvicorn.run(
        'app.app:app',
        host=settings.server_host,
        port=settings.server_port,
        reload=True,
    )
