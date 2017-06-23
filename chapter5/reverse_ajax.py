from chapter3.downloader import Downloader
import json
import lxml.html
import csv

FIELDS = ('area', 'population', )
seed_url = "http://example.webscraping.com"


def reverse_ajax():
    writer = csv.writer(open('countries.csv', 'w'))
    writer.writerow(FIELDS)

    template_url = "http://example.webscraping.com/places/ajax/search.json?&search_term={}&page_size={}&page=0"

    D = Downloader()
    html = D(template_url.format(".", 2))

    ajax = json.loads(html)

    for record in ajax['records']:
        # print(lxml.html.fromstring(record['pretty_link']).cssselect("div a")[0].get("href"))
        inner_html = D(seed_url + lxml.html.fromstring(record['pretty_link']).cssselect("div a")[0].get("href"))
        inner_tree = lxml.html.fromstring(inner_html)
        result = []
        for field in FIELDS:
            result.append(inner_tree.cssselect('table > tr#places_{0}__row > td.w2p_fw'.format(field))[
                0].text_content())
        writer.writerow(result)
