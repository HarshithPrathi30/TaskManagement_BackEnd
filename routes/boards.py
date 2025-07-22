from aiohttp import web
import asyncio
from models import fetch_all_boards, create_board, delete_board, get_board_by_id, update_board, fetch_tasks_for_board, fetch_boards_with_tasks_joined

async def get_boards_with_tasks(request):
    try:
        rows = await fetch_boards_with_tasks_joined()

        boards_dict = {}
        for row in rows:
            board_id = row[0]
            if board_id not in boards_dict:
                boards_dict[board_id] = {
                    "id": board_id,
                    "name": row[1],
                    "description": row[2],
                    "tasks": []
                }

            task_id = row[3]
            if task_id is not None:
                boards_dict[board_id]["tasks"].append({
                    "id": task_id,
                    "boardId": row[7],
                    "title": row[4],
                    "description": row[5],
                    "status": row[6]
                })

        return web.json_response(boards_dict)

    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=500)

async def get_boards(request):
    try:
        boards = await fetch_all_boards()
        return web.json_response([{"id": b[0], "name": b[1], "description": b[2]} for b in boards])
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=500)

async def post_board(request):
    try:
        data = await request.json()
        if 'name' not in data or not data['name'].strip():
            return web.json_response({"success": False, "error": "Name is required"}, status=400)

        board = await create_board(data['name'], data.get('description', ''))
        return web.json_response({"success": True, "board": {"id": board[0], "name": board[1], "description": board[2]}})
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=500)
    
async def patch_board(request):
    try:
        data = await request.json()
        if 'name' not in data or not data['name'].strip():
            return web.json_response({"success": False, "error": "Name is required"}, status=400)
        
        if 'id' not in data or not data['id']:
            board = await create_board(data['name'], data.get('description', ''))
            return web.json_response({"success": True, "board": {"id": board[0], "name": board[1], "description": board[2]}})
        else:
            board = await get_board_by_id(data['id'])
            if not board:
                return web.json_response({"success": True, "id": data['id'], "error": "Board not found or already deleted, hence can't update."})
            updatedBoard = await update_board(data['id'], data['name'], data.get('description', ''))
            return web.json_response({"success": True, "board": {"id": updatedBoard[0], "name": updatedBoard[1], "description": updatedBoard[2]}})
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=500)
    
async def delete_board_handler(request):
    try:
        board_id = request.match_info['board_id']
        board = await get_board_by_id(board_id)
        if not board:
            return web.json_response({"success": True, "id": board_id, "error": "Board not found or already deleted"})

        await delete_board(board_id)
        return web.json_response({"success": True, "id": board_id})
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=500)

# def setup_routes(app):
#     app.router.add_get('/boards', get_boards)
#     app.router.add_get('/boards-with-tasks', get_boards_with_tasks)
#     app.router.add_post('/boards', post_board)
#     app.router.add_delete('/boards/{board_id}', delete_board_handler)
def setup_routes(app):
    routes = [
        app.router.add_get('/boards', get_boards),
        app.router.add_get('/boards-with-tasks', get_boards_with_tasks),
        app.router.add_post('/boards', post_board),
        app.router.add_patch('/boards', patch_board),
        app.router.add_delete('/boards/{board_id}', delete_board_handler)
    ]
    return routes
