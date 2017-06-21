import urllib2
import re

def download(url, user_agent='wswp', num_retries=2):
    print 'Downloading: ', url

    headers = {'User-agent': user_agent}
    request = urllib2.Request(url, headers=headers)

    try:
        html = urllib2.urlopen(request).read()
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                return download(url, user_agent, num_retries-1)
    return html


def crawl_sitemap(url):
    # download the sitemap file
    sitemap = download(url)
    # extract the sitemap links
    links = re.findall('<loc>(.*?)</loc>', sitemap)
    # download each link
    for link in links:
        html = download(link)
        print html


seed_url = "http://example.webscraping.com/{0}"

if __name__ == '__main__':
    crawl_sitemap(seed_url.format("sitemap.xml"))