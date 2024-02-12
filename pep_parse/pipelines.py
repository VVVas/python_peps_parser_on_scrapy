# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter

import csv
import datetime as dt
from collections import defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATETIME_FORMAT = '%Y-%m-%dT%H-%M-%S'


class PepParsePipeline:
    """Сбор статистики об используемых статусах PEP."""

    def open_spider(self, spider):
        """Начало работы спайдера: создание словаря."""
        self.status_counts = defaultdict(int)

    def process_item(self, item, spider):
        """Обработка данных отдельного PEP."""
        self.status_counts[item['status']] += 1
        return item

    def close_spider(self, spider):
        """Завершение работы спайдера: запись в файл."""
        self.status_summary = [('Статус', 'Количество')]
        self.status_summary.extend(self.status_counts.items())
        self.status_summary.append(('Total', sum(self.status_counts.values())))

        results_dir = BASE_DIR / 'results'
        results_dir.mkdir(exist_ok=True)

        now = dt.datetime.now(dt.timezone.utc)
        now_formatted = now.strftime(DATETIME_FORMAT)
        file_name = f'status_summary_{now_formatted}.csv'

        file_path = results_dir / file_name

        with open(file_path, 'w', encoding='utf-8') as f:
            writer = csv.writer(f, dialect='unix', quoting=csv.QUOTE_NONE)
            writer.writerows(self.status_summary)
