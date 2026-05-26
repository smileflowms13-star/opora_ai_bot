from aiogram import Router, F
from aiogram.types import Message

from keyboards import relationships_menu, exercises_menu

router = Router()

@router.message(F.text == "💬 Поговорить")
async def talk_button(message: Message):
    await message.answer(
        "Напиши, что сейчас происходит.\n\n"
        "Можно коротко, например:\n"
        "«Мне тревожно»\n"
        "«Я поссорилась с партнёром»\n"
        "«Меня триггерит игнор»\n"
        "«Я устал и ничего не хочу»\n\n"
        "Скоро мы подключим AI, и я смогу отвечать более гибко."
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
        "Конечно. Напиши:\n\n"
        "1. Кому сообщение?\n"
        "2. Что произошло?\n"
        "3. Что ты хочешь донести?\n"
        "4. В каком тоне нужно: мягко / спокойно / с границей / коротко?\n\n"
        "Пока AI не подключён, я дам базовый шаблон:\n\n"
        "«Мне важно сказать о ___. Когда происходит ___, я чувствую ___. "
        "Мне бы хотелось ___. Давай обсудим, как нам лучше поступить?»"
    )

@router.message(F.text == "🌿 Упражнения")
async def exercises_button(message: Message):
    await message.answer(
        "Выбери упражнение:",
        reply_markup=exercises_menu
    )