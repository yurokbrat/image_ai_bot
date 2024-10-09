import logging

from aiogram import Dispatcher, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery

from enums import AIChoice
from generate_image import generate_image
from keyboards import ai_keyboard
from states import GenerateImageState

dp = Dispatcher(storage=MemoryStorage())
router = Router()
logger = logging.getLogger(__name__)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Привет, {message.from_user.first_name}! "  # type: ignore[union-attr]
        f"Я могу генерировать изображения по твоему текстовому описанию."
    )
    await message.answer(
        "Чтобы начать, напиши команду /generate. \n"
        "Помни, чем лучше будет твой запрос - тем лучше и будет результат :)\n"
        "Чтобы посмотреть пример хороших запросов, введи команду /example"
    )


@dp.message(Command("example"))
async def command_example_handler(message: Message) -> None:
    await message.answer(
        "Хорошо, что ты решил посмотреть примеры! Вот несколько запросов, "
        "которые выглядят идеально \n"
        "– Сильный крупный план одного глаза, прямой фронтальный вид. "
        "Детализированная радужная оболочка глаза и зрачок. Четкий акцент на "
        "текстуре и цвете глаз. Естественное освещение для передачи подлинного "
        "блеска и глубины глаз. \n\n"
        "– Солнечная система с ярко окрашенными планетами и экзотическими "
        "атмосферами, изображенная в научно-фантастическом стиле. HD, 8k, яркие"
        " цвета, HDR-эффект, цветовая палитра. \n\n"
        "– Аниме/мультяшный персонаж Headshot, детали сильно выражены и очень "
        "хорошо отображены, но при этом она выглядит, как настоящий человек.\n"
    )


@dp.message(Command("generate"))
async def handle_ai_choice(message: Message, state: FSMContext) -> None:
    await state.set_state(GenerateImageState.ai_type)
    await message.answer(
        "Выбери нейросеть:", reply_markup=ai_keyboard.as_markup()
    )


@router.callback_query(AIChoice.filter())
async def handle_prompt(
    query: CallbackQuery, callback_data: AIChoice, state: FSMContext
) -> None:
    await state.update_data(ai_type=callback_data.ai_code)
    await query.message.answer(  # type: ignore[union-attr]
        f"Ты выбрал {callback_data.ai_label.name.capitalize()}. \n"
        f"Теперь введи запрос:"
    )
    await state.set_state(GenerateImageState.prompt)
    await query.answer()


@router.message(GenerateImageState.prompt)
async def handle_prompt_input(message: Message, state: FSMContext) -> None:
    generating_message = await message.answer("Генерируем...")
    logger.info("Start generating image")
    await process_prompt(message, state, generating_message)


@router.message(GenerateImageState.prompt)
async def process_prompt(
    message: Message, state: FSMContext, generating_message: Message
) -> None:
    try:
        data = await state.update_data(prompt=message.text)
        if (prompt := data.get("prompt")) and (ai_type := data.get("ai_type")):
            await state.clear()
            try:
                image = generate_image(prompt, ai_type)
                if image:
                    await message.answer_photo(
                        photo=image,
                        caption=f"Вот изображение по твоему запросу «{prompt}»",
                    )
                    await message.answer(
                        "Чтобы снова сгенерировать изображение, "
                        "введи команду /generate."
                    )
                    await generating_message.delete()
            except Exception as error:
                error_message = f"Error occurred in generating image: {error}"
                logging.exception(error_message)
                await message.answer(
                    "Не удалось сгенерировать изображение. Попробуй позже."
                )
        else:
            current_state = await state.get_state()
            if current_state is None:
                return

            logging.info("Cancelling state %r", current_state)
            await state.clear()
            await message.answer(
                "Произошла ошибка! Пожалуйста, попробуй ещё раз"
            )
    except Exception as error:
        error_message = f"Error occurred in generating image: {error}"
        logging.exception(error_message)
        await state.clear()
        await message.answer("Произошла ошибка! Пожалуйста, попробуй ещё раз")
