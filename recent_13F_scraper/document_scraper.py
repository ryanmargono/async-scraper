import bs4
import requests
import csv

from utilities import *

class DocumentScraper:

    def __init__(self):
        self.base_url = 'https://www.sec.gov'
            
    def scrape_recent_13F(self, ticker, fields):
        print ('scraping: {}'.format(ticker))
        self.ticker = ticker
        self.fields = fields

        link = '{}/cgi-bin/browse-edgar?CIK={}'.format(self.base_url, self.ticker)
        
        res = requests.get(link)
    
        all_docs_page = bs4.BeautifulSoup(res.text, 'html.parser')
        recent_doc_link = find_doc_link(all_docs_page, self.base_url)
        recent_doc_page = bs4.BeautifulSoup(requests.get(recent_doc_link).text, 'html.parser')
        info_link = find_info_link(recent_doc_page, self.base_url)
        info_table = bs4.BeautifulSoup(requests.get(info_link).content, 'xml')

        self.write_to_tsv(scrape_table(info_table, self.fields))
    
    def write_to_tsv(self, data):
        print ('writing: {}'.format(self.ticker))
        with open ('{}_recent_13F.tsv'.format(self.ticker), 'w') as outfile:
            tsv_writer = csv.writer(outfile, delimiter='\t')
            tsv_writer.writerow(self.fields)
            for record in data:
                row_data = [ record.get(field, '') for field in self.fields ]
                tsv_writer.writerow(row_data)