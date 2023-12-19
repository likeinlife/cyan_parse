import csv
import logging
import time
import unicodedata
from pathlib import Path
from typing import Any

import requests
from pydantic import BaseModel, TypeAdapter

BASE_URL = (
    "https://api.cian.ru/valuation-offer-history/v4/get-house-offer-history-desktop/"
)

logging.basicConfig(
    format="%(levelname)s :: %(asctime)s :(%(funcName)s) %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


class Price(BaseModel):
    price: str


class Offer(BaseModel):
    id: int
    title: str
    prices: Price
    dateStart: str
    dateEnd: str | None = None
    previewPhoto: str | None = None
    link: str | None = None


class HouseInfo(BaseModel):
    totalCount: int
    roomCounts: list[Any]
    statusCounts: list[Any]
    locations: list[Any]
    offers: list[Offer]


class InitialHouseInfo(BaseModel):
    id: int
    address: str
    house: str | None


class TransformedOffer(BaseModel):
    id: int
    price: int
    area: float
    room_count: int
    floor_number: str
    address: str
    house: str | None
    link: str | None


def get_content_by_id(ad_id: int):
    """Use cyan api."""
    body = {
        "offerId": ad_id,
        "resultsOnPage": 100,
        "page": 1,
        "dealType": "sale",
        "isNearby": False,
    }
    response = requests.post(BASE_URL, json=body)
    content = response.content
    logger.debug("Request SUCCESSFUL")
    return TypeAdapter(HouseInfo).validate_json(content)


def filter_dateStart(
    ad: Offer,
    needed_month: list[str],
    needed_year: list[str],
) -> bool:
    if not ad.dateEnd:
        return False
    _, month, year = ad.dateEnd.split(" ")
    if month in needed_month and year in needed_year:
        logger.debug("FILTER: ok. %s" % ad.id)
        return True
    logger.debug("FILTER: bad. %s" % ad.id)
    return False


def transform_offer(offer: Offer, initial_info: InitialHouseInfo) -> TransformedOffer:
    title_unicode = unicodedata.normalize("NFKD", offer.title)
    logger.debug("TRANSFORM: unicode %s" % title_unicode)
    area, room_count, floor_number = title_unicode.split(", ")
    area = float(area.split(" ")[0].replace(",", "."))
    room_count = int(room_count.split("-")[0])
    floor_number = floor_number.split(" ")[0]
    price_string = offer.prices.price
    price = int(price_string.split(",")[0]) * 1000000

    link = f"https://www.cian.ru{offer.link}" or offer.previewPhoto

    return TransformedOffer(
        id=offer.id,
        price=price,
        area=area,
        room_count=room_count,
        floor_number=floor_number,
        address=initial_info.address,
        house=initial_info.house,
        link=link,
    )


def parse_old_ads(
    csv_path: Path,
    initial_list: list[InitialHouseInfo],
    needed_month: list[str],
    needed_year: list[str],
):
    counter = 0
    with open(csv_path, "w", encoding="UTF-8") as file_obj:
        headers = [
            "floor_number",
            "house",
            "address",
            "room_count",
            "area",
            "price",
            "link",
        ]
        csv_writer = csv.DictWriter(file_obj, headers, delimiter=";")
        csv_writer.writeheader()
        for init_info in initial_list:
            house_counter = 0
            MAX_HOUSE_COUNTER = 4
            offer = get_content_by_id(init_info.id)
            for offer in offer.offers:
                if not filter_dateStart(
                    ad=offer,
                    needed_month=needed_month,
                    needed_year=needed_year,
                ):
                    continue
                transformed = transform_offer(offer, init_info)
                csv_writer.writerow(transformed.model_dump(exclude={"id"}))
                house_counter += 1
                counter += 1
                logger.info("CSV: write row %d %s" % (counter, offer.id))
                if house_counter > MAX_HOUSE_COUNTER:
                    break
            if counter > 50:
                print("SUCCESS")
                break
            time.sleep(5)


def parse_csv(file_path: Path) -> list[InitialHouseInfo]:
    with open(file_path, "r", encoding="UTF-8") as file_obj:
        reader = csv.DictReader(file_obj, delimiter=";")
        return [InitialHouseInfo(**info) for info in reader]  # type: ignore


def main():
    file_path = Path("Cyan-upd.csv")
    content = parse_csv(file_path)
    new_csv_path = Path("csv-cyan-transformed1.csv")
    needed_month = ["апр", "май", "июн", "июл", "авг", "сен"]
    needed_year = ["2023"]
    parse_old_ads(
        csv_path=new_csv_path,
        initial_list=content,
        needed_month=needed_month,
        needed_year=needed_year,
    )


if __name__ == "__main__":
    main()
