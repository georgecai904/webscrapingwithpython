import threading
from chapter4.downloader import Downloader
import re, time

from chapter4.mongo_queue import MongoQueue


def threaded_crawler(seed_url, user_agent='wswp', delay=1,
                     scrape_callback=None, cache_callback=None, max_threads=10, proxies=[], num_retries=2, timeout=10):
    # the queue of URL's that still need to be crawled
    # crawl_queue =
    crawl_queue = MongoQueue()
    for url in scrape_callback(seed_url):
        crawl_queue.push(url)

    # the URL's that has been seen
    D = Downloader(cache=cache_callback, delay=delay, user_agent=user_agent, proxies=proxies, num_retries=num_retries,
                   timeout=timeout)

    def process_queue():
        try:
            url = crawl_queue.pop()
            D(url)
            crawl_queue.complete(url)
        except KeyError:
            pass

    threads = []
    while threads or crawl_queue:
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


import multiprocessing


def process_link_crawler(*args, **kwargs):
    print args, kwargs
    num_cpus = multiprocessing.cpu_count()
    print('Starting {} processes'.format(num_cpus))
    processes = []
    for i in range(num_cpus):
        p = multiprocessing.Process(target=threaded_crawler, args=args, kwargs=kwargs)
        p.start()
        processes.append(p)
    # wait for processes to complete
    for p in processes:
        p.join()