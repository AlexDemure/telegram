from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode

from src.apps.clickup.logic import (
    get_user_folders_by_space_id, get_lists_by_folder, get_user_spaces, get_data_for_burndown_chart
)
from src.apps.users.logic import get_user
from src.bot.dispatcher import bot, dp
from src.bot.keyboards import start as start_keyboards
from src.bot.keyboards.clickup import analytics
from src.bot.keyboards.clickup import menu as menu_click_up_keyboards
from src.bot.keyboards.clickup import tasks as tasks_click_up_keyboards
from src.bot.states.clickup.analytics import BurndownChartState
from src.submodules.clickup.schemas import SpaceData


@dp.message_handler(Text(equals=[menu_click_up_keyboards.MenuClickUpKeysEnum.analytics.value]), state="*")
async def start_analytics_menu(message: types.Message, state: FSMContext):
    """
    Главное меню с Аналитикой ClickUp
    :return: Клавиатуру с выбором типа Аналитики
    """
    await state.reset_state()

    user = await get_user(message.chat.id)
    if not user:
        await message.reply(
            f"Такой пользователь не найден.\nПожалуйста подключите занова ClickUp.",
            reply_markup=start_keyboards.keyboards
        )
        return

    await message.answer(
        f"Меню по Аналитике ClickUp:",
        parse_mode=ParseMode.HTML,
        reply_markup=analytics.keyboards
    )


@dp.message_handler(Text(equals=[analytics.AnalyticsClickUpKeysEnum.burndown_chart.value]), state=None)
async def burndown_chart_by_sprint_choose_space(message: types.Message):
    """
    Handler по нажатию Кнопки "Линейная диаграмма Burndown".

    :return: Возвращает InlineButtons.
    Ожидается выбор пользователя и уведомление на callback handler.
    """
    user = await get_user(message.chat.id)
    if not user:
        await message.reply(
            f"Такой пользователь не найден.\nПожалуйста подключите занова ClickUp.",
            reply_markup=start_keyboards.keyboards
        )
        return

    data = await get_user_spaces(user)
    choices = tasks_click_up_keyboards.generate_inline_buttons_for_click_up_spaces(data)
    for choice in choices:
        await bot.send_message(
            message.chat.id,
            f"{choice['team_name']}",
            reply_markup=choice['keyboards']
        )

    await BurndownChartState.choose_space.set()


async def burndown_chart_by_sprint_choose_folder(message: types.Message, state: FSMContext):
    """
    Шаг №2 Выбор папки.
    Получение списка задач по проекту.

    Функция которая вызывается из Callback Handler, burndown_chart_choose_space.
    Ожидается выбор пользователя и уведомление на callback handler.
    """
    user = await get_user(message.chat.id)
    if not user:
        await message.reply(
            f"Такой пользователь не найден.\nПожалуйста подключите занова ClickUp.",
            reply_markup=start_keyboards.keyboards
        )
        return

    data = await state.get_data()

    folders = await get_user_folders_by_space_id(user, data['space_id'])

    choice = tasks_click_up_keyboards.generate_inline_buttons_for_click_up_folders(
        SpaceData(
            id=data['space_id'],
            name=data['space_name'],
            folders=folders
        )
    )

    await bot.send_message(
        message.chat.id,
        f"{data['space_name']}",
        reply_markup=choice
    )

    await BurndownChartState.choose_folder.set()


async def burndown_chart_by_sprint_choose_list(message: types.Message, state: FSMContext):
    """
    Шаг №3 Выбор списка (bugs, backlogs, sprint) из откуда хотим взять задачи.
    Функция которая вызывается из Callback Handler, burndown_chart_choose_folder

    :return: Список InlineButtons.
    Ожидается выбор пользователя и уведомление на callback handler.
    """
    user = await get_user(message.chat.id)
    if not user:
        await message.reply(
            f"Такой пользователь не найден.\nПожалуйста подключите занова ClickUp.",
            reply_markup=start_keyboards.keyboards
        )
        return

    data = await state.get_data()

    folder_lists = await get_lists_by_folder(user, data['folder_id'])
    choice = tasks_click_up_keyboards.generate_inline_buttons_for_click_up_lists(folder_lists)

    await bot.send_message(message.chat.id, f"{folder_lists.name}", reply_markup=choice['keyboards'])

    await BurndownChartState.choose_list.set()


async def get_burndown_chart_by_sprint(message: types.Message, state: FSMContext):
    """
    Шаг №4
    Функция которая вызывается из Callback Handler, burndown_chart_choose_list

    :return: Jpeg изображение с диаграммой.
    """
    user = await get_user(message.chat.id)
    if not user:
        await message.reply(
            f"Такой пользователь не найден.\nПожалуйста подключите занова ClickUp.",
            reply_markup=start_keyboards.keyboards
        )
        return

    data = await state.get_data()

    data = await get_data_for_burndown_chart(user, data['list_id'])

    await bot.send_message(message.chat.id, f"Hello", reply_markup=analytics.keyboards)

    await state.finish()
