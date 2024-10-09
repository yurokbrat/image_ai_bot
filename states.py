from aiogram.fsm.state import StatesGroup, State


class GenerateImageState(StatesGroup):
    ai_type = State()
    prompt = State()
