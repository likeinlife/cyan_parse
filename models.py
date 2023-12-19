from typing import Any

from pydantic import BaseModel


class Price(BaseModel):
    price: str


class Offer(BaseModel):
    """Модель для хранения непосредственно архивных данных."""

    id: int
    title: str
    prices: Price
    dateStart: str
    dateEnd: str | None = None
    previewPhoto: str | None = None
    link: str | None = None


class HouseInfo(BaseModel):
    """Модель ответа с архивными записями."""

    totalCount: int
    roomCounts: list[Any]
    statusCounts: list[Any]
    locations: list[Any]
    offers: list[Offer]


class InitialHouseInfo(BaseModel):
    """Модель для хранения данных о доме из начального объявления."""

    id: int
    address: str
    house: str | None


class TransformedOffer(BaseModel):
    """Данные из модели дампятся в финальный csv."""

    id: int
    price: int
    area: float
    room_count: int
    floor_number: str
    address: str
    house: str | None
    link: str | None
