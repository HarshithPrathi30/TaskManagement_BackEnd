from aiohttp import web
from models import fetch_tasks_for_board, create_task, update_task, delete_task, get_task_by_id, get_board_by_id

async def get_tasks(request):
    try:
        board_id = request.match_info['board_id']
        board = await get_board_by_id(board_id)
        if not board:
            return web.json_response({"success": False, "error": "Board not found or deleted"}, status=404)

        tasks = await fetch_tasks_for_board(board_id)
        return web.json_response({"success": True, "tasks": [{"id": t[0], "boardId": t[1], "title": t[2], "description": t[3], "status": t[4]} for t in tasks]})
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=500)

async def post_task(request):
    try:
        board_id = request.match_info['board_id']
        data = await request.json()
        if 'title' not in data or not data['title'].strip():
            return web.json_response({"success": False, "error": "Title is required"}, status=400)

        board = await get_board_by_id(board_id)
        if not board:
            return web.json_response({"success": False, "error": "Board not found or deleted"}, status=404)

        task = await create_task(board_id, data['title'], data.get('description', ''), data.get('status', 'Not Completed'))
        return web.json_response({"success": True, "task": {
            "id": task[0], "boardId": task[1], "title": task[2], "description": task[3], "status": task[4]
        }})
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=500)

async def patch_task(request):
    try:
        task_id = request.match_info['task_id']
        task = await get_task_by_id(task_id)
        if not task:
            return web.json_response({"success": False, "error": "Task not found or deleted"}, status=404)

        data = await request.json()
        if not data['title']:
            return web.json_response({"error": "Title is required"}, status=400)

        updated = await update_task(task_id, data['title'], data['description'], data['status'])
        return web.json_response({"success": True, "task": {
            "id": updated[0], "boardId": updated[1], "title": updated[2], "description": updated[3], "status": updated[4]
        }})
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=500)

async def delete_task_handler(request):
    try:
        task_id = request.match_info['task_id']
        task = await get_task_by_id(task_id)
        if not task:
            return web.json_response({"success": True, "id": task_id, "error": "Task not found or already deleted"})

        await delete_task(task_id)
        return web.json_response({"success": True, "id": task_id})
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)

def setup_routes(app):
    app.router.add_get('/boards/{board_id}/tasks', get_tasks)
    app.router.add_post('/boards/{board_id}/tasks', post_task)
    app.router.add_patch('/tasks/{task_id}', patch_task)
    app.router.add_delete('/tasks/{task_id}', delete_task_handler)

def setup_routes(app):
    routes = [
        app.router.add_get('/boards/{board_id}/tasks', get_tasks),
        app.router.add_post('/boards/{board_id}/tasks', post_task),
        app.router.add_patch('/tasks/{task_id}', patch_task),
        app.router.add_delete('/tasks/{task_id}', delete_task_handler)
    ]
    return routes
