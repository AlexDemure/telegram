from aiogram.types import ParseMode
from aiohttp import web

from src.apps.clickup.logic import add_click_up_data_by_user
from src.apps.hubstaff.logic import add_hub_staff_data_by_user
from src.bot.commands.dispatcher import bot
from src.bot.keyboards.clickup import menu as clickup_keyboards
from src.bot.keyboards.hubstaff import menu as hubstaff_keyboards
from src.core.enums import ServicesEnum
from src.submodules.oauth.webhooks import login_success


async def login_success_to_system(request):
    """Уведомление об успешной авторизации в сервисе."""
    try:
        code, state = login_success(request)
    except ValueError as e:
        return web.json_response(status=400, data=dict(msg=str(e)))

    if state['system'] == ServicesEnum.hub_staff.value:
        await add_hub_staff_data_by_user(state['user_id'], code)
        keyboards = hubstaff_keyboards.keyboards

    elif state['system'] == ServicesEnum.click_up.value:
        await add_click_up_data_by_user(state['user_id'], code)
        keyboards = clickup_keyboards.keyboards
    else:
        raise ValueError

    await bot.send_message(
        state['user_id'],
        "Пользователь успешно добавлен.\nВыберите пункт из меню:",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboards
    )

    return web.json_response(status=200, data=dict(msg="User is add."))
