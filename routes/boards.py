from aiohttp import web
import asyncio
from models import fetch_all_boards, create_board, delete_board, get_board_by_id, update_board, fetch_tasks_for_board

async def get_boards_with_tasks(request):
    try:
        boards = await fetch_all_boards()

        async def attach_tasks(board):
            board_id = board[0]
            tasks = await fetch_tasks_for_board(board_id)
            return board_id, {
                "id": board[0],
                "name": board[1],
                "description": board[2],
                "tasks": [
                    {
                        "id": t[0],
                        "boardId": t[1],
                        "title": t[2],
                        "description": t[3],
                        "status": t[4]
                    } for t in tasks
                ]
            }

        boards_with_tasks = await asyncio.gather(*[attach_tasks(b) for b in boards])
        response = {board_id: board_data for board_id, board_data in boards_with_tasks}
        return web.json_response(response)

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
