import urlparse

from chapter1.throttle import Throttle
import random
import urllib2


class Downloader:
    def __init__(self, delay=5, user_agent='wswp', proxies=None, num_retries=1, cache=None):
        self.throttle = Throttle(delay=delay)
        self.user_agent = user_agent
        self.proxies = proxies
        self.num_retries = num_retries
        self.cache = cache

    def __call__(self, url):
        result = None

        if self.cache:
            try:
                result = self.cache[url]
            except KeyError:
                # url is not available in cache
                pass
            else:
                # It is useful for code that must be executed if the try clause does not raise an exception.
                if self.num_retries > 0 and 500 <= result['code'] < 600:
                    # server error so ignore result from cache and re-download
                    result = None

        if result is None:
            # result was not loaded from cache so still need to download
            self.throttle.wait(url)
            proxy = random.choice(self.proxies) if self.proxies else None
            headers = {'User-agent': self.user_agent}
            result = self.download(url, headers, proxy, self.num_retries)
            if self.cache:
                # save result to cache
                self.cache[url] = result
        # print(result)
        return result['html']

    def download(self, url, headers, proxy, num_retries):
        print 'Downloading: ', url

        code = 0
        request = urllib2.Request(url, headers=headers)

        # Build up proxy
        opener = urllib2.build_opener()
        if proxy:
            proxy_params = {urlparse.urlparse(url).scheme: proxy}
            opener.add_handler(urllib2.ProxyHandler(proxy_params))

        try:
            # User proxy opener
            html = opener.open(request).read()
            code = 200
        except urllib2.URLError as e:
            print 'Download error:', e.reason
            html = None
            if num_retries > 0:
                if hasattr(e, 'code') and 500 <= e.code < 600:
                    return self.download(url, headers, proxy, num_retries - 1)
            else:
                code = 404

        return {'html': html, 'code': code}

