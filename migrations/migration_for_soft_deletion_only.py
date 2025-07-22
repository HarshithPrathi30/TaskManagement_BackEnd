import aiosqlite
import asyncio

DB_PATH = 'database.db'

async def migrate():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("ALTER TABLE boards ADD COLUMN is_deleted INTEGER DEFAULT 0")
        await db.execute("ALTER TABLE tasks ADD COLUMN is_deleted INTEGER DEFAULT 0")
        await db.commit()

asyncio.run(migrate())