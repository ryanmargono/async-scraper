import bs4
import requests

def find_doc_link(soup, base_url):
    doc = soup.find(lambda tag: tag.name == 'td' and '13F' in tag.text)
    return '{}{}'.format(base_url, doc.parent.find('a')['href'])

def find_info_link(doc_page, base_url):
    info_link = doc_page.find(lambda tag: tag.name=='a' and '.xml' in tag.text and not 'primary_doc' in tag.text)
    return '{}{}'.format(base_url, info_link['href'])

def scrape_table(info_table, fields):
    data = info_table.findAll('infoTable')
    result = []
    for record in data:
        entry = { field: record.find(field).text  if record.find(field) else '' for field in fields }
        result.append(entry)
    return result