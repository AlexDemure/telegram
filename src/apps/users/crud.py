from src.db.database import users_db


async def get_user(user_id: int):
    return await users_db.collection.find_one({'user_id': user_id})


async def add_user(data: dict):
    return await users_db.collection.insert_one(data)




