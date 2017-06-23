import threading
from chapter4.downloader import Downloader
import re, time


def threaded_crawler(seed_url, user_agent='wswp', delay=1,
                     scrape_callback=None, cache_callback=None, max_threads=10, proxies=[], num_retries=2, timeout=10):
    # the queue of URL's that still need to be crawled
    crawl_queue = scrape_callback(seed_url)

    # the URL's that has been seen
    D = Downloader(cache=cache_callback, delay=delay, user_agent=user_agent, proxies=proxies, num_retries=num_retries,
                   timeout=timeout)

    def process_queue():
        if crawl_queue:
            url = crawl_queue.pop()
            D(url)
    # D("http://www.baidu.com")
    # for url in crawl_queue:
    #     D(url)
    threads = []
    while threads or crawl_queue:
        # print(threads, crawl_queue)
        # the crawl is still active
        for thread in threads:
            if not thread.is_alive():
                # remove the stopped thread
                threads.remove(thread)

        while len(threads) < max_threads and crawl_queue:
            # can start some more threads
            thread = threading.Thread(target=process_queue)
            # set daemon so main thread can exit when receives ctrl-c
            thread.setDaemon(True)
            thread.start()
            threads.append(thread)

        # all threads have been processed
        # sleep temporarily so CPU can focus execution elsewhere
        time.sleep(1)


def _get_links(html):
    """ Return a list of links from html"""

    # a regular expression to extract all links from the webpage
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    # list of all links from the webpage
    return webpage_regex.findall(html)
