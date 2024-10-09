import fal_client
from deep_translator import GoogleTranslator


def generate_image(prompt: str, ai_type: str) -> str | None:
    translated_prompt = GoogleTranslator(source="auto", target="en").translate(
        text=prompt
    )
    handler = fal_client.submit(
        ai_type,
        arguments={"prompt": translated_prompt, "enable_safety_checker": False},
    )
    if images := handler.get().get("images"):
        return images[0].get("url")
    return None
