from aiogram import Router, F
from aiogram.types import Message

from keyboards import relationships_menu, exercises_menu

router = Router()

@router.message(F.text == "💬 Поговорить")
async def talk_button(message: Message):
    await message.answer(
        "Я здесь, чтобы выслушать. Расскажи, что у тебя на душе.\n\n"
        "Можешь описать ситуацию, чувства или просто мысли, которые приходят в голову. "
        "Я постараюсь понять и поддержать тебя."
    )

@router.message(F.text == "💔 Отношения")
async def relationships_button(message: Message):
    await message.answer(
        "Отношения часто цепляют самые чувствительные места.\n\n"
        "Выбери, что ближе:",
        reply_markup=relationships_menu
    )

@router.message(F.text == "💔 Меня игнорируют")
async def ignored_button(message: Message):
    await message.answer(
        "Понимаю. Когда важный человек долго не отвечает, тревога может резко подниматься.\n\n"
        "Давай разделим факты и интерпретации.\n\n"
        "Факт: человек не отвечает.\n\n"
        "Интерпретация может быть:\n"
        "— «я ему/ей не нужен/не нужна»;\n"
        "— «меня бросят»;\n"
        "— «я сделал/сделала что-то не так»;\n"
        "— «со мной что-то не так».\n\n"
        "Какая мысль звучит сильнее всего?"
    )

@router.message(F.text == "😡 Я ревную")
async def jealousy_button(message: Message):
    await message.answer(
        "Ревность часто возникает там, где есть страх потерять связь, безопасность или значимость.\n\n"
        "Давай начнём мягко:\n\n"
        "Что именно запустило ревность?\n"
        "Например: сообщение, лайк, молчание, встреча, сравнение, фантазия?"
    )

@router.message(F.text == "🥶 Партнёр холодный")
async def cold_partner_button(message: Message):
    await message.answer(
        "Когда партнёр кажется холодным, это может сильно задевать.\n\n"
        "Давай уточним:\n\n"
        "Что именно ты называешь холодностью?\n"
        "— мало пишет;\n"
        "— не проявляет нежность;\n"
        "— избегает разговоров;\n"
        "— обесценивает;\n"
        "— пропадает;\n"
        "— другое?"
    )

@router.message(F.text == "🧲 Не могу отпустить")
async def cannot_let_go_button(message: Message):
    await message.answer(
        "Отпустить бывает сложно не потому, что ты слабый/слабая, а потому что привязанность не выключается по команде.\n\n"
        "Первый вопрос:\n\n"
        "Что именно сложнее всего отпустить?\n"
        "— человека;\n"
        "— надежду;\n"
        "— образ будущего;\n"
        "— чувство вины;\n"
        "— незавершённый разговор?"
    )

@router.message(F.text == "🧨 Мы постоянно ссоримся")
async def conflicts_button(message: Message):
    await message.answer(
        "Повторяющиеся ссоры часто идут по одному сценарию.\n\n"
        "Давай найдём цикл:\n\n"
        "1. С чего обычно начинается ссора?\n"
        "2. Что ты делаешь дальше?\n"
        "3. Что делает другой человек?\n"
        "4. Чем всё заканчивается?\n\n"
        "Можешь ответить свободно одним сообщением."
    )

@router.message(F.text == "🚧 Хочу поставить границу")
async def boundary_button(message: Message):
    await message.answer(
        "Граница — это не нападение, а способ сохранить контакт и уважение к себе.\n\n"
        "Мягкая формула:\n\n"
        "«Когда происходит ___, я чувствую ___. Мне важно ___. Поэтому я прошу/буду ___».\n\n"
        "Напиши ситуацию, и я помогу сформулировать границу."
    )

@router.message(F.text == "✉️ Помоги написать сообщение")
async def help_write_message_button(message: Message):
    await message.answer(
        "Конечно, давай вместе составим текст.\n\n"
        "Опиши, пожалуйста:\n"
        "— Кому ты хочешь написать?\n"
        "— Что случилось?\n"
        "— Какую главную мысль хочешь донести?\n"
        "— Какой тон будет уместным (мягкий, спокойный, решительный)?\n\n"
        "Я помогу подобрать слова и выстроить сообщение."
    )

@router.message(F.text == "🌿 Упражнения")
async def exercises_button(message: Message):
    await message.answer(
        "Выбери упражнение:",
        reply_markup=exercises_menu
    )

# Временные статические упражнения (позже будут заменены на интерактивные FSM)
@router.message(F.text == "🛑 STOP")
async def stop_exercise(message: Message):
    await message.answer(
        "Техника STOP\n\n"
        "S — Stop: остановись.\n"
        "T — Take a breath: сделай медленный вдох и выдох.\n"
        "O — Observe: заметь, что происходит в теле, мыслях и эмоциях.\n"
        "P — Proceed: выбери следующий маленький шаг.\n\n"
        "Вопрос: какой самый бережный следующий шаг ты можешь сделать сейчас?"
    )

@router.message(F.text == "🎯 Зона контроля")
async def control_zone_exercise(message: Message):
    await message.answer(
        "Упражнение «Зона контроля»\n\n"
        "Раздели ситуацию на 3 части:\n\n"
        "1. Что я не контролирую?\n"
        "2. На что я могу повлиять?\n"
        "3. Какой один маленький шаг я могу сделать сегодня?\n\n"
        "Это помогает снизить накручивание и вернуть ощущение опоры."
    )

@router.message(F.text == "💛 Самосострадание")
async def self_compassion_exercise(message: Message):
    await message.answer(
        "Упражнение «Самосострадание»\n\n"
        "Положи руку на грудь или живот.\n\n"
        "Скажи себе:\n\n"
        "«Мне сейчас трудно».\n"
        "«Я не обязан/обязана справляться идеально».\n"
        "«Я могу быть к себе мягче хотя бы на 1%».\n\n"
        "Сделай 3 медленных выдоха."
    )