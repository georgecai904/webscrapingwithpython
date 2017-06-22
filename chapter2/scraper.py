
import urllib
import datetime
FIELDS = ('area', 'population',)

import re
def regex_scraper(html):
    results = {}
    for field in FIELDS:
        pattern = '<tr id="places_{0}__row">.*?<td class="w2p_fw">(.*?)</td>'.format(field)
        results[field] = re.search(pattern, html).groups()[0]
    return results


from bs4 import BeautifulSoup
def bs4_scraper(html):
    soup = BeautifulSoup(html, 'html.parser')
    results = {}
    for field in FIELDS:
        results[field] = soup.find('table').find('tr', id='places_{0}__row'.format(field)).find('td', class_='w2p_fw').text
    return results


import lxml.html
def lxml_scraper(html):
    tree = lxml.html.fromstring(html)
    results = {}
    for field in FIELDS:
        results[field] = tree.cssselect('table > tr#places_{0}__row > td.w2p_fw'.format(field))[0].text_content()
    return results


if __name__ == '__main__':
    url = 'http://example.webscraping.com/places/default/view/Afghanistan-1'
    html = urllib.urlopen(url).read()
    a = datetime.datetime.now()
    print(regex_scraper(html))
    b = datetime.datetime.now()
    print(bs4_scraper(html))
    c = datetime.datetime.now()
    print(lxml_scraper(html))
    d = datetime.datetime.now()
    print(b-a, c-b, d-c)
