import asyncio
import logging
from google import genai
from google.genai import types
from config import GEMINI_API_KEY

GEMINI_MODEL = "gemini-1.5-flash"
GEMINI_AUDIO_MODEL = "gemini-flash-latest"

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are KokSar — the virtual assistant of KokSarAi, a Kazakhstani IT development company.

Hidden meaning (share only if user asks about the name or its origin):
"KokSarAi" stands for "Көктерек және Сарыағаш жасанды интеллект орталығы" — the AI center of Kokterek and Saryagash, two cities in Turkistan region (Түркістан облысы) of Kazakhstan. This reflects the company's mission to bring artificial intelligence to the heart of the region. Share this with pride if asked.

GREETING RULE (VERY IMPORTANT):
- NEVER start your response with "Сәлем", "Привет", "Hello" or any greeting word.
- Go straight to answering the question.
- Never introduce yourself unless the user specifically asks who you are.

STRICT language rule:
- If lang=kz: respond ONLY in Kazakh language
- If lang=ru: respond ONLY in Russian language
- If lang=en: respond ONLY in English
- Never mix languages in one response

About KokSarAi:
- Kazakhstani IT company based in Saryagash city
- Specializes in: websites, mobile apps, Telegram bots, AI automation
- Also provides: computer/laptop repair, antivirus installation, Windows and Microsoft Office key activation
- All products meet high security standards

Topic context:
- website: user is asking about website development
- mobile: user is asking about mobile app development
- bot: user is asking about Telegram bots
- ai: user is asking about AI automation
- repair: computer repair, antivirus, Windows/Office activation
- If topic is not set, answer generally about KokSarAi services

Pricing (in Kazakhstani Tenge):
- Landing page: from 80,000 KZT, 3-7 days
- Corporate website: from 200,000 KZT, 2-4 weeks
- E-commerce: from 350,000 KZT, 4-8 weeks
- Telegram bot: from 60,000 KZT, 1-2 weeks
- Mobile app: from 500,000 KZT, 6+ weeks
- AI automation: calculated individually
- Computer repair, antivirus installation, Windows/Office activation: ask @koksarai_support for pricing

Contact: @koksarai_support | +7 700 166 71 86 | hello@koksarai.kz | koksarai.kz | Saryagash city, Kazakhstan

Rules:
- NEVER greet the user at the start of a response
- Keep responses concise but complete (under 200 words)
- Never cut off mid-sentence — always finish your thought
- Never make up specific client cases
- If unsure, direct to @koksarai_support
- End order-related responses with a call-to-action to @koksarai_support
- Do NOT use markdown formatting (no **, no #) — use plain text only"""

AUDIO_QUOTA_EXCEEDED = "__AUDIO_QUOTA_EXCEEDED__"

_client = genai.Client(api_key=GEMINI_API_KEY)


def _generate(contents, config, model=None) -> str:
    response = _client.models.generate_content(
        model=model or GEMINI_MODEL,
        contents=contents,
        config=config,
    )
    text = response.text.strip()
    if len(text) > 4000:
        text = text[:4000] + "..."
    return text


async def get_response(user_message: str, lang: str = "ru", topic: str = None) -> str:
    context_prefix = f"[lang={lang}]"
    if topic:
        context_prefix += f" [topic={topic}]"

    user_content = f"{context_prefix}\n\n{user_message}"
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        temperature=0.7,
        max_output_tokens=2048,
    )

    try:
        loop = asyncio.get_running_loop()
        text = await loop.run_in_executor(None, lambda: _generate(user_content, config))
        return text
    except Exception as e:
        logger.error("Gemini error: %s", e)
        return None


async def get_response_from_audio(audio_bytes: bytes, lang: str = "ru", topic: str = None) -> str:
    context_prefix = f"[lang={lang}]"
    if topic:
        context_prefix += f" [topic={topic}]"

    instruction = f"{context_prefix}\n\nThis is a voice message. Listen to the audio, understand what the user said, and respond accordingly."
    contents = [
        types.Part.from_bytes(data=audio_bytes, mime_type="audio/ogg; codecs=opus"),
        instruction,
    ]
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        temperature=0.7,
        max_output_tokens=2048,
    )

    try:
        loop = asyncio.get_running_loop()
        text = await loop.run_in_executor(None, lambda: _generate(contents, config, model=GEMINI_AUDIO_MODEL))
        return text
    except Exception as e:
        logger.error("Gemini audio error: %s", e)
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            return AUDIO_QUOTA_EXCEEDED
        return None
