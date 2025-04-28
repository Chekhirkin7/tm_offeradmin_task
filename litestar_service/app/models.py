import asyncio
import uuid
from enum import Enum

from sqlalchemy import (
    String,
    ForeignKey,
    Enum as SQLAlchemyEnum,
    Text,
    UniqueConstraint,
    Boolean,
    Integer,
    UUID,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from .db import sessionmanager


class Base(DeclarativeBase):
    pass


class OfferChoices(Enum):
    Loanplus = "Loanplus"
    SgroshiCPA2 = "SgroshiCPA2"
    Novikredyty = "Novikredyty"
    TurboGroshi = "TurboGroshi"
    Crypsee = "Crypsee"
    Suncredit = "Suncredit"
    Lehko = "Lehko"
    Monto = "Monto"
    Limon = "Limon"
    Amigo = "Amigo"
    FirstCredit = "FirstCredit"
    Finsfera = "Finsfera"
    Pango = "Pango"
    Treba = "Treba"
    StarFin = "StarFin"
    BitCapital = "BitCapital"
    SgroshiCPL = "SgroshiCPL"
    LoviLave = "LoviLave"
    Prostocredit = "Prostocredit"
    Sloncredit = "Sloncredit"
    Clickcredit = "Clickcredit"
    Credos = "Credos"
    Dodam = "Dodam"
    SelfieCredit = "SelfieCredit"
    Egroshi = "Egroshi"
    Alexcredit = "Alexcredit"
    SgroshiCPA1 = "SgroshiCPA1"
    Tengo = "Tengo"
    Credit7 = "Credit7"
    Tpozyka = "Tpozyka"
    Creditkasa = "Creditkasa"
    Moneyveo = "Moneyveo"
    My_Credit = "MyCredit"
    Credit_Plus = "CreditPlus"
    Miloan = "Miloan"
    Avans = "AvansCredit"


class OfferWall(Base):
    __tablename__ = "admin_panel_offerwall"

    token: Mapped[UUID] = mapped_column(
        UUID, primary_key=True, default=uuid.uuid4, unique=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=True)
    url: Mapped[str] = mapped_column(String(200), nullable=True, default=None)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    offer_assignments: Mapped[list["OfferWallOffer"]] = relationship(
        back_populates="offer_wall_rel", cascade="all, delete-orphan"
    )
    popup_assignments: Mapped[list["OfferWallPopupOffer"]] = relationship(
        back_populates="offer_wall_rel", cascade="all, delete-orphan"
    )

    def __str__(self):
        return f"OfferWall {self.token}"


class Offer(Base):
    __tablename__ = "admin_panel_offer"

    uuid: Mapped[UUID] = mapped_column(
        UUID, primary_key=True, default=uuid.uuid4, unique=True
    )
    id: Mapped[int] = mapped_column(Integer, nullable=True)
    url: Mapped[str] = mapped_column(String(200), nullable=True, default=None)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    name: Mapped[OfferChoices] = mapped_column(
        SQLAlchemyEnum(OfferChoices), unique=True
    )
    sum_to: Mapped[str] = mapped_column(String(255), nullable=True, default=None)
    term_to: Mapped[int] = mapped_column(Integer, nullable=True, default=None)
    percent_rate: Mapped[int] = mapped_column(Integer, nullable=True, default=None)

    wall_assignments: Mapped[list["OfferWallOffer"]] = relationship(
        back_populates="offer_rel", cascade="all, delete-orphan"
    )
    popup_assignments: Mapped[list["OfferWallPopupOffer"]] = relationship(
        back_populates="offer_rel", cascade="all, delete-orphan"
    )

    def __str__(self):
        return self.name.value


class OfferWallOffer(Base):
    __tablename__ = "admin_panel_offerwalloffer"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order: Mapped[int] = mapped_column(Integer, default=0)
    offer_id: Mapped[UUID] = mapped_column(
        ForeignKey("admin_panel_offer.uuid", ondelete="CASCADE")
    )
    offer_wall_id: Mapped[UUID] = mapped_column(
        ForeignKey("admin_panel_offerwall.token", ondelete="CASCADE")
    )

    offer_wall_rel: Mapped["OfferWall"] = relationship(
        back_populates="offer_assignments"
    )
    offer_rel: Mapped["Offer"] = relationship(back_populates="wall_assignments")

    __table_args__ = (
        UniqueConstraint("offer_wall_id", "offer_id", name="uq_offerwall_offer"),
    )

    def __repr__(self):
        return f"<OfferWallOffer offer_id={self.offer_id} wall_id={self.offer_wall_id} order={self.order}>"


class OfferWallPopupOffer(Base):
    __tablename__ = "admin_panel_offerwallpopupoffer"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order: Mapped[int] = mapped_column(Integer, default=0)
    offer_id: Mapped[UUID] = mapped_column(
        ForeignKey("admin_panel_offer.uuid", ondelete="CASCADE")
    )
    offer_wall_id: Mapped[UUID] = mapped_column(
        ForeignKey("admin_panel_offerwall.token", ondelete="CASCADE")
    )

    offer_wall_rel: Mapped["OfferWall"] = relationship(
        back_populates="popup_assignments"
    )
    offer_rel: Mapped["Offer"] = relationship(back_populates="popup_assignments")

    __table_args__ = (
        UniqueConstraint("offer_wall_id", "offer_id", name="uq_offerwallpopup_offer"),
    )

    def __repr__(self):
        return f"<OfferWallPopupOffer offer_id={self.offer_id} wall_id={self.offer_wall_id} order={self.order}>"


async def drop_tables():
    engine = sessionmanager._engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def create_tables():
    engine = sessionmanager._engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def main():
    await drop_tables()
    await create_tables()


if __name__ == "__main__":
    asyncio.run(main())
