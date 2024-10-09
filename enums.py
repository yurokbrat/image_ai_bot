from enum import Enum

from aiogram.filters.callback_data import CallbackData


class AIType(str, Enum):
    standard = "Standard"
    pro = "Pro"
    realism = "Realism"
    abstraction = "Abstraction"
    cartoon = "Cartoon"


class AICode(str, Enum):
    dev = "fal-ai/flux/dev"
    pro = "fal-ai/flux-pro/v1.1"
    realism = "fal-ai/flux-realism"
    aura_flow = "fal-ai/aura-flow"
    sote_diffusion = "fal-ai/stable-cascade/sote-diffusion"


class AIChoice(CallbackData, prefix="ai_choice"):
    ai_label: AIType
    ai_code: AICode
