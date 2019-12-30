#!/usr/bin/env python

from document_scraper import DocumentScraper
from scrapy.crawler import CrawlerProcess
import sys


ticker = str(sys.argv[1])
sort = bool(sys.argv[2])
fields = ['nameOfIssuer', 'titleOfClass', 'cusip', 'value', 'sshPrnamt', 'sshPrnamtType', 'putCall', 'investmentDiscretion', 'otherManager', 'Sole', 'Shared', 'None']

process = CrawlerProcess({
'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
'LOG_LEVEL': 'ERROR',
})

process.crawl(DocumentScraper, ticker=ticker, fields=fields, sort=sort)
process.start()