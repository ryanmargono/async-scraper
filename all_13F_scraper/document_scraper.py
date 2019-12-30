import scrapy
from scrapy import Request, selector
import csv

class DocumentScraper(scrapy.Spider):
    name = "DocumentScraper"
    
    def __init__(self, *args, **kwargs):
        super(DocumentScraper, self).__init__(*args, **kwargs) 
        print ("scraping: {}".format(self.ticker))

        self.base_url = 'https://www.sec.gov'
        self.data = []

        self.sort = kwargs.get('sort')
        self.ticker = kwargs.get('ticker')
        self.fields = kwargs.get('fields')
        self.start_urls = [ '{}/cgi-bin/browse-edgar?CIK={}'.format(self.base_url, self.ticker) ]
        

    def parse(self, response):
        next_page = response.css('input[value="Next 40"]::attr(onclick)').get()
        if next_page:
            next_page_url = '{}{}'.format(self.base_url, next_page.replace('parent.location=', '').strip("'"))
            yield Request(next_page_url, callback = self.parse)

        doc_links = response.xpath("//td[contains(text(), '13F')]/following-sibling::td[1]/a/@href").getall()
        for link in doc_links:
            yield Request('{}{}'.format(self.base_url, link), callback=self.parse_doc_page)

    def parse_doc_page(self, response):
        xml_link = response.xpath("//td[contains(text(), 'INFORMATION TABLE')]/preceding-sibling::td[1]/a[contains(text(), '.xml')]/@href").get()
        date = response.xpath("//div[contains(text(), 'Filing Date')]/following-sibling::div[1]/text()").get()
        if xml_link:
            yield Request('{}{}'.format(self.base_url, xml_link), callback=self.parse_info_table, meta={'date': date})
    
    def parse_info_table(self, response):
        rows = response.xpath("//*[local-name()='infoTable']")
        for row in rows:
            record = { field: row.xpath(".//*[local-name()='{}']/text()".format(field)).get() if row.xpath(".//*[local-name()='{}']/text()".format(field)).get() else '' for field in self.fields }
            record['date'] = response.meta['date']
            self.data.append(record)
    
    def closed(self, reason):
        print ("writing to tsv: {}".format(self.ticker))
        if (self.sort): 
            self.data = sorted(self.data, key=lambda i:i['date'], reverse=True)
        with open ('{}_13F.tsv'.format(self.ticker), 'w') as outfile:
            tsv_writer = csv.writer(outfile, delimiter='\t')
            fields = [ 'date' ] + self.fields
            tsv_writer.writerow(fields)
            for record in self.data:
                row_data = [ record.get(field, '') for field in fields ]
                tsv_writer.writerow(row_data)
