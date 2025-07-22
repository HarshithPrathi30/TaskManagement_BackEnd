from db import DB_PATH
import aiosqlite

async def fetch_all_boards():
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT * FROM boards WHERE is_deleted = 0")
        return await cursor.fetchall()

async def create_board(name, description):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT INTO boards (name, description) VALUES (?, ?)", (name, description))
        await db.commit()
        cursor = await db.execute("SELECT * FROM boards WHERE id = last_insert_rowid()")
        return await cursor.fetchone()
    
async def update_board(id, name, description):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE boards SET name = ?, description = ? WHERE id = ?", 
            (name, description, id)
        )
        await db.commit()
        cursor = await db.execute("SELECT * FROM boards WHERE id = ?", (id,))
        return await cursor.fetchone()

async def get_board_by_id(board_id):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT * FROM boards WHERE id = ? AND is_deleted = 0", (board_id,))
        return await cursor.fetchone()

async def delete_board(board_id):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE boards SET is_deleted = 1 WHERE id = ?", (board_id,))
        await db.commit()

async def fetch_tasks_for_board(board_id):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT * FROM tasks WHERE board_id = ? AND is_deleted = 0", (board_id,))
        return await cursor.fetchall()

async def get_task_by_id(task_id):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT * FROM tasks WHERE id = ? AND is_deleted = 0", (task_id,))
        return await cursor.fetchone()

async def create_task(board_id, title, description, status):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT INTO tasks (board_id, title, description, status) VALUES (?, ?, ?, ?)", (board_id, title, description, status))
        await db.commit()
        cursor = await db.execute("SELECT * FROM tasks WHERE id = last_insert_rowid()")
        return await cursor.fetchone()

async def update_task(task_id, title, description, status):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE tasks SET title = ?, description = ?, status = ? WHERE id = ?", (title, description, status, task_id))
        await db.commit()
        cursor = await db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        return await cursor.fetchone()

async def delete_task(task_id):
    async with aiosqlite.connect(DB_PATH) as db:
        # await db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        db.execute("UPDATE tasks SET is_deleted = 1 WHERE id = ?", (task_id,))
        await db.commit()