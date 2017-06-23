from zipfile import ZipFile
from StringIO import StringIO
from chapter3.downloader import Downloader
import csv


class AlexaCallback:
    """This class is used to download top 1 million websites csv file from alexa"""
    def __init__(self, max_urls=5):
        self.max_urls = max_urls
        self.seed_url = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'

    # def __call__(self, url):
    #     """Download from link"""
    #     if url == self.seed_url:
    #         urls = []
    #         D = Downloader()
    #         zipped_data = D(url)
    #         with ZipFile(StringIO(zipped_data)) as zf:
    #             csv_filename = zf.namelist()[0]
    #             for _, website in csv.reader(zf.open(csv_filename)):
    #                 urls.append("http://{0}".format(website))
    #                 if len(urls) == self.max_urls:
    #                     break
    #
    #         return urls

    def __call__(self, offline_filename):
        urls = []
        with open(offline_filename, "r") as csvfile:
            for _, website in csv.reader(csvfile):
                urls.append("http://{0}".format(website))
                if len(urls) == self.max_urls:
                    break
        return urls
