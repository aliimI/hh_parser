import httpx
from config import settings


class TGClient:
    def __init__(self):
        self._client = httpx.AsyncClient(timeout=20.0)

    async def close(self):
        await self._client.aclose()

    async def send_message(self, text: str) -> None:
        url = f"https://api.telegram.org/bot{settings.TG_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": settings.TG_CHAT_ID,
            "text": text,
            "disable_web_page_preview": False,
        }
        r = await self._client.post(url, json=payload)
        r.raise_for_status()