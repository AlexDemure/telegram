from bson import ObjectId

from src.db.database import users_db


async def _get_user(user_id: int):
    return await users_db.collection.find_one({'user_id': user_id})


async def _add_user(data: dict):
    return await users_db.collection.insert_one(data)


async def _get_users() -> list:
    users = list()
    async for document in users_db.collection.find():
        users.append(document)

    return users


async def update_document(document_id: ObjectId, document_data: dict):
    return await users_db.collection.replace_one(
        {'_id': document_id},
        document_data
    )
