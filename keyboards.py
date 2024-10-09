from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from enums import AIChoice, AICode, AIType

builder = InlineKeyboardBuilder()

ai_keyboard = builder.add(
    InlineKeyboardButton(
        text="Standard",
        callback_data=AIChoice(
            ai_label=AIType.standard, ai_code=AICode.dev
        ).pack(),
    ),
    InlineKeyboardButton(
        text="Pro",
        callback_data=AIChoice(ai_label=AIType.pro, ai_code=AICode.pro).pack(),
    ),
    InlineKeyboardButton(
        text="Realism",
        callback_data=AIChoice(
            ai_label=AIType.realism, ai_code=AICode.realism
        ).pack(),
    ),
    InlineKeyboardButton(
        text="Abstraction",
        callback_data=AIChoice(
            ai_label=AIType.abstraction, ai_code=AICode.aura_flow
        ).pack(),
    ),
    InlineKeyboardButton(
        text="Cartoon",
        callback_data=AIChoice(
            ai_label=AIType.cartoon, ai_code=AICode.sote_diffusion
        ).pack(),
    ),
)

ai_keyboard.adjust(1)
