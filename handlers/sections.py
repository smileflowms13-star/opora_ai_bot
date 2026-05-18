from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from keyboards import relationships_menu, exercises_menu, settings_menu


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


@router.message(Command("diary"))
@router.message(F.text == "📝 Дневник")
async def diary_button(message: Message):
    await message.answer(
        "Дневник помогает увидеть повторяющиеся состояния и триггеры.\n\n"
        "Ответь одним сообщением:\n\n"
        "1. Настроение от 1 до 10:\n"
        "2. Тревога от 1 до 10:\n"
        "3. Энергия от 1 до 10:\n"
        "4. Как спал/спала: плохо / нормально / хорошо\n"
        "5. Что сегодня сильнее всего повлияло на состояние?"
    )


@router.message(F.text == "🌿 Упражнения")
async def exercises_button(message: Message):
    await message.answer(
        "Выбери упражнение:",
        reply_markup=exercises_menu
    )


@router.message(F.text == "🌬 Дыхание 4–6")
async def breathing_exercise(message: Message):
    await message.answer(
        "Упражнение «Дыхание 4–6»\n\n"
        "Подходит при тревоге, напряжении, перегрузе.\n\n"
        "1. Сядь удобно.\n"
        "2. Поставь стопы на пол.\n"
        "3. Сделай вдох на 4 счёта.\n"
        "4. Сделай выдох на 6 счётов.\n"
        "5. Повтори 6–8 раз.\n\n"
        "После этого заметь: стало ли легче хотя бы на 1%?"
    )


@router.message(F.text == "👀 5–4–3–2–1")
async def grounding_exercise(message: Message):
    await message.answer(
        "Упражнение «5–4–3–2–1»\n\n"
        "Помогает вернуться в настоящий момент.\n\n"
        "Назови:\n\n"
        "5 предметов, которые видишь;\n"
        "4 ощущения в теле;\n"
        "3 звука;\n"
        "2 запаха;\n"
        "1 вкус или одну вещь, которая сейчас в безопасности.\n\n"
        "Делай медленно. Не нужно идеально."
    )


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


@router.message(F.text == "✍️ Письмо без отправки")
async def unsent_letter_exercise(message: Message):
    await message.answer(
        "Письмо без отправки\n\n"
        "Это способ выпустить эмоции безопасно.\n\n"
        "Напиши письмо человеку или ситуации, не отправляя его.\n\n"
        "Начни так:\n"
        "«Я злюсь, потому что…»\n"
        "«Мне больно, потому что…»\n"
        "«Я хотел/хотела бы, чтобы…»\n"
        "«Сейчас мне важно…»\n\n"
        "После письма сделай паузу 10 минут."
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





@router.message(F.text == "⚙️ Настройки")
async def settings_button(message: Message):
    await message.answer(
        "Настройки:",
        reply_markup=settings_menu
    )