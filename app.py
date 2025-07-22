from aiohttp import web
import aiohttp_cors
from routes import boards, tasks
from db import init_db
from pathlib import Path
from aiohttp.web_exceptions import HTTPNotFound
import os
from dotenv import load_dotenv

load_dotenv()

FRONTEND_PATH = os.getenv("FRONTEND_PATH", "Frontend/frontend/public/index.html")

async def spa_handler(request):
    index_file = Path(FRONTEND_PATH)
    if index_file.exists():
        return web.FileResponse(str(index_file))
    raise HTTPNotFound()

@web.middleware
async def catch_all_handler(request, handler):  #Is useful when frontend is built and served by the backend. Currently has no effect but will be helpful in future if modified. 
    try:
        response = await handler(request)
        if response.status == 404 and request.method == 'GET':
            return await spa_handler(request)
        return response
    except web.HTTPException as ex:
        if ex.status == 404 and request.method == 'GET':
            return await spa_handler(request)
        raise

async def init_app():
    app = web.Application(middlewares=[catch_all_handler, web.normalize_path_middleware(merge_slashes=True)])
    await init_db()

    boards.setup_routes(app)
    tasks.setup_routes(app)

    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods=["GET", "POST", "DELETE", "PATCH", "OPTIONS"],
        )
    })
    for route in list(app.router.routes()):
        cors.add(route)

    return app

web.run_app(init_app(), port=8000)