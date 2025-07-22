import aiosqlite

DB_PATH = 'database.db'

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        with open('schema.sql') as f:
            await db.executescript(f.read())
        await db.commit()