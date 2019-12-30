#!/usr/bin/env python

from document_scraper import DocumentScraper
import sys

ticker = str(sys.argv[1])

scraper = DocumentScraper()
fields = ['nameOfIssuer', 'titleOfClass', 'cusip', 'value', 'sshPrnamt', 'sshPrnamtType', 'putCall', 'investmentDiscretion', 'otherManager', 'Sole', 'Shared', 'None']
scraper.scrape_recent_13F(ticker, fields)