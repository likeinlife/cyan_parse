# Описание

Персер архивных объявлений из циана. На выходе получается csv файл с архивными объявлениями и ценами, за которые они были проданы.

# Использование

1. `pip install -r requirements.txt`
2. Скачать архив с нужными записями об квартирах с циана
3. Полученный excel файл сохранить как csv с кодировкой utf-8, положить в директорию с кодом
4. В config.py при необходимости поменять значение переменной CYAN_FILENAME на csv-файл
5. Запустить transform_csv.py
6. Запустить house_info.py

На выходе будет csv-файл с дефолтным названием cyan-archive.csv (можно заменить в config.py CYAN_ARCHIVE_FILENAME)

# Настройка

Константы в config.py:

- MAX_ADS (default - 50): Максимальное количество архивных записей в файле
- MAX_ADS_PER_HOUSE (default - 4): Максимальное количество архивных записей на дом
- NEEDED_MONTH (default - ["апр", "май", "июн", "июл", "авг", "сен"]): Нужные месяца архивных записей
- NEEDED_YEAR (default - ["2023"]): Нужный год архивных записей
- LOGGING_LEVEL (default - logging.INFO): Уровень логирования. Если что-то сломалось, можно попробовать отследить ошибку, поменяв INFO на DEBUG

- CYAN_FILENAME (default - Path("cyan.csv")): Название начального файла циана(который перевели из excel формата)
- CYAN_TRANSFORMED_FILENAME (default - Path("cyan-upd.csv")): Название трансформированного csv-файла
- CYAN_ARCHIVE_FILENAME (default - Path("cyan-archive.csv")): Название csv-файла с архивными записями