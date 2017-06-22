import os
import datetime
import time

if __name__ == "__main__":
    cache_dir = os.path.join(os.path.dirname(__file__), "cache")
    url = 'http://example.webscraping.com/places/default/view/Afghanistan-1'

    """[Test] Chapter3 downloader"""
    # from chapter3.downloader import Downloader
    # D = Downloader()
    # D('http://example.webscraping.com/places/default/view/Afghanistan-1')

    """[Test] Chapter3 crawler"""
    # from chapter3.crawler import link_crawler
    # link_crawler("http://example.webscraping.com/", "/places/default/view/")

    """[Test] Chapter 3 disk_cache url_to_path"""  # from chapter3.disk_cache import DiskCache
    # dc = DiskCache(cache_dir=cache_dir)
    # dc._url_to_path(url=url)

    """[Test] Chapter 3 disk_cache getter & setter"""
    # from chapter3.disk_cache import DiskCache
    # from chapter3.downloader import Downloader
    # dc = DiskCache(cache_dir=cache_dir)
    # downloader = Downloader()
    # dc[url] = downloader(url)
    # print(dc[url])

    """[Test] Chapter 3 disk_cache expires"""
    # from chapter3.disk_cache import DiskCache
    # from chapter3.downloader import Downloader

    # dc = DiskCache(cache_dir=cache_dir, expires=datetime.timedelta(seconds=5))
    # downloader = Downloader()
    # dc[url] = downloader(url)
    # print(dc[url])
    # time.sleep(5)
    # print(dc[url])

    """[Test] Chapter 3 mongodb"""
    from chapter3.mongo_cache import MongoCache
    from chapter3.downloader import Downloader
    mc = MongoCache(expires=datetime.timedelta(seconds=10))
    downloader = Downloader()
    mc[url] = downloader(url)
    # mc[url]
    # time.sleep(70)
    # print(mc[url])

