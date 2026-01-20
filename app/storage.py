import logging

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Vacancy

log = logging.getLogger(__name__)

class Storage:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    
    async def save_new(self, v: dict) -> bool:
        row = Vacancy(
            hh_id = str(v["id"]),
            title = v.get("name") or "",
            url = v.get("alternate_url")  or "",
            employer = (v.get("employer") or {}).get("name"),
            area=(v.get("area") or {}).get("name"),
            salary=_format_salary(v.get("salary")),
        )
        self.session.add(row)
        try:
            await self.session.commit()
            log.info("Saved vacancy hh_id=%s", row.hh_id)
            return True
        except IntegrityError:
            await self.session.rollback()
            return False
        
    async def get_unsent(self, limit: int = 50) -> list[Vacancy]:
        q = select(Vacancy).where(Vacancy.sent_to_tg == False).order_by(Vacancy.id.desc()).limit(limit)
        res = await self.session.execute(q)
        return list(res.scalars().all())
        

    async def mark_sent(self, vacancy_id: int) -> None:
        q = update(Vacancy).where(Vacancy.id == vacancy_id).values(sent_to_tg=True)
        await self.session.execute(q)
        await self.session.commit()
        


def _format_salary(s: dict | None) -> str | None:
    if not s:
        return None
    cur = s.get("currency")
    f, t = s.get("from"), s.get("to")
    if f and t:
        return f"{f}-{t} {cur}"
    if f:
        return f"from {f} {cur}"
    if t:
        return f"to {t} {cur}"
    return None