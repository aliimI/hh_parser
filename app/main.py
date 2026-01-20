import asyncio
import logging
from app.log_config import setup_logging

from app.db import async_session_maker
from app.hh_client import HHClient
from app.tg_client import TGClient
from app.fetcher import Fetcher
from app.storage import Storage

setup_logging(logging.INFO)

log = logging.getLogger(__name__)

def format_message(v) -> str:
    parts = [
        f"{v.title}",
        f"{v.employer or '—'} | {v.area or '—'}",
        f"Salary: {v.salary or '—'}",
        v.url,
    ]
    return "\n".join(parts)

async def run_once():
    hh = HHClient()
    tg = TGClient()
    try:
        fetcher = Fetcher(hh)

        async with async_session_maker() as session:
            store = Storage(session)

            raw_items = await fetcher.fetch_all()

          
            for it in raw_items:
                
                await store.save_new(it)

            unsent = await store.get_unsent(limit=30)
            for v in reversed(unsent):
                await tg.send_message(format_message(v))
                await store.mark_sent(v.id)

    finally:
        await hh.close()
        await tg.close()

async def main_loop():
    from app.config import settings
    while True:
        await run_once()
        await asyncio.sleep(settings.RUN_EVERY_MIN * 60)

if __name__ == "__main__":
    asyncio.run(main_loop())