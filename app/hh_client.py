import httpx
from app.config import settings


class HHClient:
    
    def __init__(self):
        self._client = httpx.AsyncClient(
            headers={"User-Agent": settings.USER_AGENT},
            timeout=20.0,
        )

    async def close(self):
        await self._client.aclose()
        
    async def search(self, text: str, page: int = 0) -> dict:
        params = {
            "text": text,
            "page": page,
            "per_page": settings.PER_PAGE,
        }

        if settings.ONLY_WITH_SALARY:
            params["only_with_salary"] = "true"

        if settings.AREAS:
            params["area"] = settings.AREAS 
        if settings.PROF_ROLES:
            params["professional_role"] = settings.PROF_ROLES
        if settings.EXPERIENCE:
            params["experience"] = settings.EXPERIENCE

        r = await self._client.get(settings.HH_API_URL, params=params)
        r.raise_for_status()
        return r.json()

