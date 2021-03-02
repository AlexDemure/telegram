from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode

from src.apps.clickup.logic import ClickUp
from src.apps.users.crud import get_user
from src.commands.dispatcher import dp
from src.keyboards import menu_keyboards
from src.apps.clickup.enums import PriorityEnumsByEmoji, TagsEnumsByEmoji


@dp.message_handler(Text(equals=["Список задач"]), state=None)
async def get_my_tasks(message: types.Message):
    user_data = await get_user(message.chat.id)
    if not user_data:
        await message.reply(f"Такой пользователь не найден.", reply_markup=menu_keyboards.keyboards)

    prepare_data = await ClickUp(user_data['auth_token']).collect_user_tasks()

    prepare_data.tasks.sort(
        key=lambda x: (
            PriorityEnumsByEmoji(x.priority).priority_value,
            [
                TagsEnumsByEmoji(x.name).priority_value for x in x.tags
            ]
        ),
        reverse=True
    )

    response = ""

    for task in prepare_data.tasks:
        tags_to_str = ""
        for tag in task.tags:
            try:
                tags_to_str += f"{TagsEnumsByEmoji(tag.name).emoji}"
            except ValueError:
                continue

        response += f"{PriorityEnumsByEmoji(task.priority).emoji}{tags_to_str} <a href='{task.url}'>{task.id}</a> {task.name}\n" \

    await message.answer(f"{response}", parse_mode=ParseMode.HTML, reply_markup=menu_keyboards.keyboards)

