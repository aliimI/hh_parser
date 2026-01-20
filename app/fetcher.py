from hh_client import HHClient

def build_queries() -> list[str]:

    from config import settings
    return settings.KEYWORDS


class Fetcher:
    def __init__(self, hh: HHClient):
        self.hh =hh


    async def fetch_all(self) -> list[dict]:
        items: list[dict] = []
        for q in build_queries():
            page = 0
            while True:
                data = await self.hh.search(text=q, page=page)
                items.extend(data.get("items", []))
                if page >= (data.get("pages", 1) - 1):
                    break
                page += 1
        return items

