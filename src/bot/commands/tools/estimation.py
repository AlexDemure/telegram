from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode

from src.apps.tools.logic import calculate_pert
from src.bot.dispatcher import dp, bot
from src.bot.keyboards.start import MainMenuKeysEnum
from src.bot.keyboards.tools.menu import MenuToolsKeysEnum, menu_keyboards
from src.bot.states.tools.estimation import TimeEstimationByPert


@dp.message_handler(Text(equals=[MainMenuKeysEnum.tools.value]), state=None)
async def start_tools_menu(message: types.Message):
    """
    Главное меню с Инструментами и Методами менеджмента.
    :return: Клавиатуру с выбором "Инструментов и методов"
    """
    await message.answer(
        f"Меню с инструментами:",
        parse_mode=ParseMode.HTML,
        reply_markup=menu_keyboards
    )


@dp.message_handler(Text(equals=[MenuToolsKeysEnum.pert.value]), state=None)
async def time_estimate_by_pert_input_values(message: types.Message):
    """
    Handler по нажатию Кнопки "Оценка времени по Pert".

    :return: Ничего не возвращает. Ожидается ввод пользователя.
    """
    response = f"Оценка времени по Pert.\n" \
               f"Формула расчета: EAD = (P + 4M +O) / 6\n" \
               f"P - «пессимистичная оценка»\n" \
               f"O - «оптимистичная оценка»\n" \
               f"M - «наиболее вероятная оценка»\n" \
               f"Вычисляемая величина - «Дни»\n\n" \
               f"Введите значения через пробел в формате Р О М (например 160 90 120):"
    await message.answer(
        response,
        parse_mode=ParseMode.HTML,
        reply_markup=menu_keyboards
    )

    await TimeEstimationByPert.add_values.set()


@dp.message_handler(state=TimeEstimationByPert.add_values)
async def time_estimate_by_pert_calculation(message: types.Message, state: FSMContext):
    """
    Подсчет оценки времени по Pert

    :return: Примерное значение.
    """
    text_items = message.text.split(" ")
    if len(text_items) != 3:
        await bot.send_message(
            message.chat.id,
            "Не удалось получить корректные значения для вычисления",
            reply_markup=menu_keyboards
        )
        await state.finish()
        return

    try:
        val_p, val_o, val_m = [float(x) for x in text_items]
    except ValueError:
        await bot.send_message(
            message.chat.id,
            "Не удалось получить корректные значения для вычисления",
            reply_markup=menu_keyboards
        )
        await state.finish()
        return

    if val_p == 0 or val_o == 0 or val_m == 0:
        await bot.send_message(
            message.chat.id,
            "Не удалось получить корректные значения для вычисления",
            reply_markup=menu_keyboards
        )
        await state.finish()
        return

    values = calculate_pert(val_p, val_o, val_m)
    response = f"Предполагаемая длительность: {'{:.1f}'.format(values[0])}\n" \
               f"Отклонение: {'{:.2f}'.format(values[1])}\n" \
               f"Диапозон отклонения: {'{:.1f}'.format(values[2])}-{'{:.1f}'.format(values[3])}"

    await bot.send_message(
        message.chat.id,
        response,
        reply_markup=menu_keyboards
    )
    await state.finish()


