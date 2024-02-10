import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        section = response.css('section#numerical-index')

        all_peps = section.css('a.pep[href^="pep-"]')
        for pep_link in all_peps:
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        pep = response.css('section#pep-content')

        pattern = r'^PEP (?P<number>\d+) – (?P<name>\w.*)'
        number, name = pep.css('h1.page-title::text').re(pattern)
        status = pep.css('dt:contains("Status") + dd abbr::text').get()

        data = {
            'number': number,
            'name': name,
            'status': status,
        }

        yield PepParseItem(data)
