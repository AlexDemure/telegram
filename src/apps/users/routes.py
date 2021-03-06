from aiogram.types import ParseMode
from aiohttp import web

from src.apps.clickup.logic import add_click_up_data_by_user
from src.apps.hubstaff.logic import add_hub_staff_data_by_user
from src.bot.commands.dispatcher import bot
from src.bot.keyboards.clickup import menu_keyboards as clickup_keyboards
from src.bot.keyboards.hubstaff import menu_keyboards as hubstaff_keyboards
from src.utils import decode_data_from_base64


async def connect_to_system(request):
    try:
        state = decode_data_from_base64(request.query.get("state"))
    except Exception:
        return web.json_response(status=400, data=dict(msg="Incorrect code. Try logging in again"))

    verify_code = request.query.get("code")

    if state['system'] == "hubstaff":
        await add_hub_staff_data_by_user(state['user_id'], verify_code)
        keyboards = hubstaff_keyboards.keyboards

    elif state['system'] == "clickup":
        await add_click_up_data_by_user(state['user_id'], verify_code)
        keyboards = clickup_keyboards.keyboards
    else:
        return web.json_response(status=400, data=dict(msg="Incorrect code. Try logging in again"))

    await bot.send_message(
        state['user_id'],
        "Пользователь успешно добавлен.\nВыберите пункт из меню:",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboards
    )

    return web.json_response(status=200, data=dict(msg="User is add."))
