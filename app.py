from aiohttp import web
import aiohttp_cors
from routes import boards, tasks
from db import init_db
from pathlib import Path
from aiohttp.web_exceptions import HTTPNotFound

async def spa_handler(request):
    index_file = Path(__file__).parent.parent / 'Frontend' / 'frontend' / 'public' / 'index.html'
    if index_file.exists():
        return web.FileResponse(str(index_file))
    raise HTTPNotFound()

async def catch_all_handler(request):
    try:
        return await spa_handler(request)
    except FileNotFoundError:
        raise HTTPNotFound()

async def init_app():
    app = web.Application()
    await init_db()

    board_routes = boards.setup_routes(app)
    task_routes = tasks.setup_routes(app)

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

    app.middlewares.append(web.normalize_path_middleware(merge_slashes=True))
    app.router.add_route('*', '/{tail:.*}', spa_handler)

    return app

web.run_app(init_app(), port=8000)