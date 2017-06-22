import os


if __name__ == "__main__":
    cache_dir = os.path.join(os.path.dirname(__file__), "cache")
    url = 'http://example.webscraping.com/places/default/view/Afghanistan-1'

    # Test Chapter3 downloader
    # from chapter3.downloader import Downloader
    # D = Downloader()
    # D('http://example.webscraping.com/places/default/view/Afghanistan-1')

    # Test Chapter3 crawler
    # from chapter3.crawler import link_crawler
    # link_crawler("http://example.webscraping.com/", "/places/default/view/")

    # Test Chapter 3 disk_cache
    from chapter3.disk_cache import DiskCache
    dc = DiskCache(cache_dir=cache_dir)
    dc.url_to_path(url=url)