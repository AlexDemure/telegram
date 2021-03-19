from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from src.bot.commands.clickup.analytics import (
    burndown_chart_by_sprint_choose_folder, burndown_chart_by_sprint_choose_list,
    get_burndown_chart_by_sprint
)
from src.bot.dispatcher import dp
from src.bot.states.clickup.analytics import BurndownChartState


@dp.callback_query_handler(text_contains="spaces", state=BurndownChartState.choose_space)
async def burndown_chart_choose_space(query: CallbackQuery, state: FSMContext):
    """
    Callback функция - принимает уведомления при выборе Space в Workspace.
    Ожидаемое состояние - Диаграмма Burndown, Выбор Space

    Space - список глобальных папок в окружении.
    query = CallbackData("spaces", "id", "name")
    """
    space = query.data.split(':')
    await state.update_data(space_id=space[1], space_name=space[2])

    await burndown_chart_by_sprint_choose_folder(query.message, state)  # Переход на этап выбор Folder из выбранного Space


@dp.callback_query_handler(text_contains="folders", state=BurndownChartState.choose_folder)
async def burndown_chart_choose_folder(query: CallbackQuery, state: FSMContext):
    """
    Callback функция - принимает уведомления при выборе Folder в Workspace.
    Ожидаемое состояние - Диаграмма Burndown, Выбор Folder

    Folder - список папок в Space окружении.
    query = CallbackData("folders", "id", "name")
    """
    folder = query.data.split(':')
    await state.update_data(folder_id=folder[1], folder_name=folder[2])

    await burndown_chart_by_sprint_choose_list(query.message, state)  # Переход на этап выбора List из выбранного Folder


@dp.callback_query_handler(text_contains="lists", state=BurndownChartState.choose_list)
async def burndown_chart_choose_list(query: CallbackQuery, state: FSMContext):
    """
    Callback функция - принимает уведомления при выборе List в Folder.
    Ожидаемое состояние - Диаграмма Burndown, Выбор List

    List - один из элементов Folder, List могут быть спринты, backlogs, bugs.
    query = CallbackData("lists", "id", "name")
    """
    list = query.data.split(':')
    await state.update_data(list_id=list[1], list_name=list[2])

    await get_burndown_chart_by_sprint(query.message, state)  # Переход на этап выбора статуса задачи.
