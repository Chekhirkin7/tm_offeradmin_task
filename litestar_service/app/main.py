from typing import Dict
from uuid import UUID
from litestar import Litestar, get, Router
from litestar.openapi import OpenAPIConfig
from sqlalchemy import select
from .schemas import OfferWallBase
from .models import OfferChoices, OfferWall
from .db import sessionmanager
from urllib.parse import urlparse
import logging

logging.basicConfig(level=logging.INFO)


def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme:
        return parsed.netloc
    else:
        return url.strip().rstrip("/")


@get("/offerwalls/{token:uuid}", response_model=OfferWallBase)
async def get_offerwall(token: UUID) -> OfferWallBase | tuple[Dict, int]:
    try:
        async with sessionmanager.session() as session:
            async with session.begin():
                stmt = select(OfferWall).filter(OfferWall.token == token)
                result = await session.execute(stmt)
                offerwall = result.scalar_one_or_none()
                if not offerwall:
                    logging.error(f"OfferWall with token {token} not found.")
                    return {"error": "OfferWall not found"}, 404

                offerwall_data = {
                    "token": offerwall.token,
                    "name": offerwall.name,
                    "url": offerwall.url,
                    "description": offerwall.description,
                }

                return OfferWallBase(**offerwall_data)
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        print(f"Error occurred: {e}")
        return {"error": "Internal server error"}, 500


@get("offerwalls/by_url/{url:str}", response_model=OfferWallBase)
async def get_offerwall_by_url(url: str) -> OfferWallBase:
    try:
        normalized_url = normalize_url(url)
        async with sessionmanager.session() as session:
            async with session.begin():
                stmt = select(OfferWall).filter(
                    OfferWall.url.like(f"%{normalized_url}%")
                )
                result = await session.execute(stmt)
                offerwall = result.scalar_one_or_none()
                if not offerwall:
                    logging.error(f"OfferWall with url {url} not found.")
                    return {"error": "OfferWall not found"}, 404
                offerwall_data = {
                    "token": offerwall.token,
                    "name": offerwall.name,
                    "url": offerwall.url,
                    "description": offerwall.description,
                }

        return offerwall_data

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return {"error": "Internal server error"}, 500


@get("/offerwalls/offer-names")
async def get_offer_names() -> Dict[str, list[str]]:
    try:
        offer_names = [offer.value for offer in OfferChoices]
        return {"offer_names": offer_names}
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return {"error": "Internal server error"}, 500


offerwall_router = Router(
    path="/api",
    route_handlers=[get_offerwall, get_offerwall_by_url, get_offer_names],
)

app = Litestar(
    route_handlers=[offerwall_router],
    openapi_config=OpenAPIConfig(title="OfferWall API", version="1.0.0"),
)
