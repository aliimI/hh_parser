from sqlalchemy import String, Integer, DateTime, Boolean, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from app.db import Base

class Vacancy(Base):
    __tablename__ = "vacancies"
    __table_args__ = (UniqueConstraint("hh_id", name="uq_vacancy_hh_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hh_id: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)
    employer: Mapped[str] = mapped_column(String, nullable=True)
    area: Mapped[str] = mapped_column(String, nullable=True)
    salary: Mapped[str] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),)
    sent_to_tg: Mapped[bool] = mapped_column(Boolean, default=False)