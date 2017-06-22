import urllib2
import re
from chapter1.throttle import Throttle
from chapter2.scrapeCallback import ScrapeCallback


def download(url, user_agent='wswp', proxy=None, num_retries=2):
    print 'Downloading: ', url

    headers = {'User-agent': user_agent}
    request = urllib2.Request(url, headers=headers)

    # Build up proxy
    opener = urllib2.build_opener()
    if proxy:
        proxy_params = {urlparse.urlparse(url).scheme: proxy}
        opener.add_handler(urllib2.ProxyHandler(proxy_params))

    try:
        # User proxy opener
        html = opener.open(request).read()
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                return download(url, user_agent, proxy, num_retries - 1)
    return html


def crawl_sitemap(url):
    # download the sitemap file
    sitemap = download(url)
    # extract the sitemap links
    links = re.findall('<loc>(.*?)</loc>', sitemap)
    # download each link
    for link in links:
        html = download(link)


import urlparse
import robotparser


def link_crawler(seed_url, link_regex, user_agent='wswp', delay=1, max_depth=2, scrape_callback=ScrapeCallback()):
    """ Crawl from the given seed URL following links matched by link_regex """

    crawl_queue = [seed_url]

    # keep track which URL's have seen before
    seen = {}


    # define a robotparser
    rp = robotparser.RobotFileParser()
    rp.set_url(seed_url + '/robots.txt')
    rp.read()

    # Set up throttle to control access waiting time
    throttle = Throttle(delay=delay)

    while crawl_queue:
        url = crawl_queue.pop()
        # check url passes robots.txt restrictions

        if rp.can_fetch(user_agent, url):
            html = download(url)

            scrape_callback(url, html)

            # control access waiting time
            throttle.wait(url=url)

            # Get the depth of current url
            depth = seen[url]

            if depth != max_depth:
                # filter for links matching our regular expression
                for link in get_links(html):
                    if re.match(link_regex, link):
                        link = urlparse.urljoin(seed_url, link)
                        if link not in seen:
                            seen[link] = depth + 1
                            crawl_queue.append(link)

        else:
            print 'Blocked by robots.txt: ', url


def get_links(html):
    """ Return a list of links from html"""

    # a regular expression to extract all links from the webpage
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    # list of all links from the webpage
    return webpage_regex.findall(html)


seed_url = "http://example.webscraping.com"

if __name__ == '__main__':
    # crawl_sitemap(seed_url+"/places/default/sitemap.xml")
    link_crawler(seed_url, '/places/default/(index|view)/')
