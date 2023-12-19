import csv
from pathlib import Path

from config import CYAN_FILENAME, CYAN_TRANSFORMED_FILENAME


def clear_room_count(room_count_string: str | None) -> int | None:
    if not room_count_string:
        return None

    if "," in room_count_string:
        return int(room_count_string.split(",")[0])
    return int(room_count_string)


def clear_area(area_string: str | None) -> float | None:
    if not area_string:
        return None
    if "/" in area_string:
        return float(area_string.split("/")[0])
    return float(area_string)


def clear_price(price_string: str | None) -> int | None:
    if not price_string:
        return None
    if " руб" in price_string:
        return int(price_string.split(" руб")[0])
    return int(price_string)


def clear_roof_and_house(
    roof_and_house_string: str | None
) -> tuple[str | None, str | None]:
    if not roof_and_house_string:
        return (None, None)
    if "," not in roof_and_house_string:
        return (roof_and_house_string, None)
    splitted = roof_and_house_string.split(", ")
    return (splitted[0], splitted[1])


def reformat_csv(old_path: Path, new_path: Path):
    with (
        open(old_path, "r", encoding="UTF-8") as old_file,
        open(new_path, "w", encoding="UTF-8") as new_file,
    ):
        reader = csv.DictReader(old_file, delimiter=";")
        field_names = [
            "id",
            "floor",
            "house",
            "address",
            "room_count",
            "area",
            "price",
            "link",
        ]
        writer = csv.DictWriter(new_file, fieldnames=field_names, delimiter=";")
        writer.writeheader()
        for i in reader:
            floor, house = clear_roof_and_house(roof_and_house_string=i["Дом"])
            ad_info = {
                "id": i["\ufeffID"],
                "room_count": clear_room_count(i["Количество комнат"]),
                "area": clear_area(i["Площадь, м2"]),
                "address": i["Адрес"],
                "price": clear_price(i["Цена"]),
                "house": house,
                "floor": floor,
                "link": i["Ссылка на объявление"],
            }
            writer.writerow(ad_info)


def main():
    reformat_csv(CYAN_FILENAME, CYAN_TRANSFORMED_FILENAME)


if __name__ == "__main__":
    main()
