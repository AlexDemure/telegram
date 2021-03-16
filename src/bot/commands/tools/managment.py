from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode

from src.bot.dispatcher import dp
from src.bot.keyboards.tools.menu import MenuToolsKeysEnum, menu_keyboards


@dp.message_handler(Text(equals=[MenuToolsKeysEnum.manager_tools.value]), state=None)
async def manager_tools(message: types.Message):
    """
    Handler по нажатию Кнопки "Список инструментов".

    :return: Список инструментов по управлению задачами.
    """
    response = f"Список инструментов по управлению задачами\n" \
               f"Управление задачами: <a href='https://clickup.com/'>ClickUp</a>\n" \
               f"Контроль времени: <a href='https://hubstaff.com/'>HubStaff</a>\n" \
               f"BMPN-схемы: <a href='http://demo.bpmn.io/'>bpmn.io</a>\n" \
               f"Визуализация прототипов: <a href='https://balsamiq.com/'>Balsamiq Wireframes</a>\n" \
               f"Онлайн-документы: <a href='https://www.google.ru/intl/ru/docs/about/'>Google Docs</a>\n"

    await message.answer(
        response,
        parse_mode=ParseMode.HTML,
        reply_markup=menu_keyboards,
        disable_web_page_preview=True
    )

