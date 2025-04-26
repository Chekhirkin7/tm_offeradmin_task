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
    func,
    UUID,
    select,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncSession
from db import sessionmanager


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
    __tablename__ = "offerwall"

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

    async def add_offer(self, offer, db: AsyncSession, order=None):
        if order is None:
            result = await db.execute(
                select(func.max(OfferWallOffer.order)).where(
                    OfferWallOffer.offer_wall_id == self.token
                )
            )
            max_order = result.scalar_one_or_none() or 0
            order = max_order + 1

        new_offer = OfferWallOffer(
            offer_wall_id=self.token,
            offer_id=offer.uuid,
            order=order,
        )

        db.add(new_offer)
        await db.commit()

    async def reorder_offers(self, offer_order_list: list, db: AsyncSession):
        for index, offer_uuid in enumerate(offer_order_list):
            await db.execute(
                OfferWallOffer.__table__.update()
                .where(
                    (OfferWallOffer.offer_wall_id == self.token)
                    & (OfferWallOffer.offer_id == offer_uuid)
                )
                .values(order=index)
            )
        await db.commit()

    async def get_offers(self, db: AsyncSession):
        result = await db.execute(
            select(OfferWallOffer)
            .where(OfferWallOffer.offer_wall_id == self.token)
            .order_by(OfferWallOffer.order)
        )
        offer_assignments = result.scalars().all()
        return [assignment.offer_rel for assignment in offer_assignments]


class Offer(Base):
    __tablename__ = "offer"

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
    __tablename__ = "offerwalloffer"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order: Mapped[int] = mapped_column(Integer, default=0)
    offer_id: Mapped[UUID] = mapped_column(ForeignKey("offer.uuid", ondelete="CASCADE"))
    offer_wall_id: Mapped[UUID] = mapped_column(
        ForeignKey("offerwall.token", ondelete="CASCADE")
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
    __tablename__ = "offerwallpopupoffer"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order: Mapped[int] = mapped_column(Integer, default=0)
    offer_id: Mapped[UUID] = mapped_column(ForeignKey("offer.uuid", ondelete="CASCADE"))
    offer_wall_id: Mapped[UUID] = mapped_column(
        ForeignKey("offerwall.token", ondelete="CASCADE")
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
