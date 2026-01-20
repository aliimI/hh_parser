import httpx
import logging

from app.config import settings

log = logging.getLogger(__name__)


class TGClient:
    def __init__(self):
        self._client = httpx.AsyncClient(timeout=20.0)
        log.info("Telegram client initialized")

    async def close(self):
        await self._client.aclose()

    async def send_message(self, text: str) -> None:
        url = f"https://api.telegram.org/bot{settings.TG_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": settings.TG_CHAT_ID,
            "text": text,
            "disable_web_page_preview": False,
        }

        log.info("Sending message to Telegram")

        r = await self._client.post(url, json=payload)
        if r.status_code >= 400:
            raise RuntimeError(f"Telegram API error {r.status_code}: {r.text}")

        r.raise_for_status()