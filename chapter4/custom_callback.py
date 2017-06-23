from chapter4.downloader import Downloader


class CustomCallback:
    def __init__(self, max_urls=5):
        self.max_urls = max_urls
        self.seed_url = 'http://alexa.chinaz.com/Country/index_CN.html'

    def __call__(self, url):
        D = Downloader()
        html = D(self.seed_url)
        import lxml.html
        tree = lxml.html.fromstring(html)
        urls = []
        for link in tree.cssselect(".rowbox li .tohome"):
            if len(urls) == self.max_urls:
                break
            urls.append(link.get("href"))
        return urls
