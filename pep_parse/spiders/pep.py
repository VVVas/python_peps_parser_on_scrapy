import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    """Спайдер парсинга PEP."""

    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        """Получение ссылок на отдельные PEP."""
        section = response.css('section#numerical-index')

        all_peps = section.css('a.pep[href^="pep-"]')
        for pep_link in all_peps:
            if pep_link.attrib['href'].endswith('/'):
                yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        """Парсинг отдельного PEP."""
        pep = response.css('section#pep-content')

        pattern = r'^PEP (?P<number>\d{1,4}) – (?P<name>\w.*)'
        number, name = pep.css('h1.page-title::text').re(pattern)
        status = pep.css('dt:contains("Status") + dd abbr::text').get()

        data = {
            'number': number,
            'name': name,
            'status': status,
        }

        yield PepParseItem(data)
