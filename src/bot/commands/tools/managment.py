from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode

from src.bot.dispatcher import dp
from src.bot.keyboards.tools.menu import MenuToolsKeysEnum, menu_keyboards
from src.submodules.common.base_class import APIClass

api = APIClass()


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


@dp.message_handler(Text(equals=[MenuToolsKeysEnum.meetings.value]), state=None)
async def meetings_list(message: types.Message):
    """
    Handler по нажатию Кнопки "Расписание".

    :return: Список встреч по продуктам.
    """
    google_doc = "https://docs.google.com/spreadsheets/d/15_rWv68gcpcYYbWex6KPTJmLu-BuJU8Y3y0T5jTbmEw/edit#gid=0"

    data = await api.make_request("GET", "https://api.steinhq.com/v1/storages/6051abc0f62b6004b3eb6776/Лист1")

    response = f"Расписание\n" \
               f"Документ с расписанием: <a href='{google_doc}'>Документ</a>\n" \

    for row in data:
        response += f"{row['day']} {row['time']} - {row['name']} (<a href='{row['url']}'>Конференция</a>)\n"

    await message.answer(
        response,
        parse_mode=ParseMode.HTML,
        reply_markup=menu_keyboards,
        disable_web_page_preview=True
    )

