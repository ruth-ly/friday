"""
Text-to-speech via ElevenLabs (primary) → OpenAI TTS (fallback).
Returns base64-encoded MP3 for the frontend to play, or None if unavailable.
"""
from __future__ import annotations
import base64
import httpx
from src.core.config import config
from src.utils.logger import logger


async def text_to_speech(text: str) -> str | None:
    if config.ELEVENLABS_API_KEY:
        result = await _elevenlabs(text)
        if result:
            return result

    if config.OPENAI_API_KEY:
        return await _openai(text)

    return None


async def _elevenlabs(text: str) -> str | None:
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{config.ELEVENLABS_VOICE_ID}"
    async with httpx.AsyncClient(timeout=20.0) as client:
        try:
            r = await client.post(
                url,
                headers={
                    "xi-api-key": config.ELEVENLABS_API_KEY,
                    "Content-Type": "application/json",
                },
                json={
                    "text": text,
                    "model_id": "eleven_monolingual_v1",
                    "voice_settings": {
                        "stability":        0.60,
                        "similarity_boost": 0.80,
                        "style":            0.10,
                        "use_speaker_boost": True,
                    },
                },
            )
            if r.status_code == 200:
                return base64.b64encode(r.content).decode()
            logger.warning(f"ElevenLabs TTS {r.status_code}: {r.text[:120]}")
        except Exception as e:
            logger.warning(f"ElevenLabs TTS error: {e}")
    return None


async def _openai(text: str) -> str | None:
    async with httpx.AsyncClient(timeout=20.0) as client:
        try:
            r = await client.post(
                "https://api.openai.com/v1/audio/speech",
                headers={"Authorization": f"Bearer {config.OPENAI_API_KEY}"},
                json={"model": "tts-1", "input": text, "voice": "nova"},
            )
            if r.status_code == 200:
                return base64.b64encode(r.content).decode()
            logger.warning(f"OpenAI TTS {r.status_code}")
        except Exception as e:
            logger.warning(f"OpenAI TTS error: {e}")
    return None
