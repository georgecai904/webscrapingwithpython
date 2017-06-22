import re
from chapter2.scrapeCallback import ScrapeCallback
from chapter3.downloader import Downloader

import urlparse
import robotparser


def link_crawler(seed_url, link_regex, user_agent='wswp', delay=1, max_depth=2, scrape_callback=ScrapeCallback(),
                 cache=None):
    """ Crawl from the given seed URL following links matched by link_regex """

    crawl_queue = [seed_url]

    # keep track which URL's have seen before
    seen = {seed_url: 0}

    # Set up robots
    rp = _get_robots(seed_url)

    downloader = Downloader(delay=delay, user_agent=user_agent, proxies=None, num_retries=3, cache=cache)

    links = []

    while crawl_queue:
        url = crawl_queue.pop()

        # Get the depth of current url
        depth = seen[url]

        if rp.can_fetch(user_agent, url):
            if depth != max_depth:
                html = downloader(url)
                scrape_callback(url, html)
                # filter for links matching our regular expression
                for link in _get_links(html):
                    if re.match(link_regex, link):
                        link = urlparse.urljoin(seed_url, link)
                        if link not in seen:
                            seen[link] = depth + 1
                            crawl_queue.append(link)
                            links.append(link)

        else:
            print 'Blocked by robots.txt: ', url

    return links


def _get_links(html):
    """ Return a list of links from html"""

    # a regular expression to extract all links from the webpage
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    # list of all links from the webpage
    return webpage_regex.findall(html)


def _get_robots(seed_url):
    # define a robot parser
    rp = robotparser.RobotFileParser()
    rp.set_url(seed_url + '/robots.txt')
    rp.read()
    return rp
