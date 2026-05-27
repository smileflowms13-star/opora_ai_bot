from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

router = Router()

@router.callback_query(F.data.startswith("quick_exercise_"))
async def quick_exercise_callback(callback: CallbackQuery, state: FSMContext):
    exercise_name = callback.data[len("quick_exercise_"):]
    await state.clear()
    # Отправляем сообщение с текстом упражнения, как если бы пользователь нажал обычную кнопку
    await callback.message.answer(exercise_name)
    await callback.answer()