from tortoise import Tortoise


async def init(DB_URL):
    await Tortoise.init(db_url=DB_URL, modules={"models": ["plateaukit.models"]})
    await Tortoise.generate_schemas()
