import urlparse
import hashlib
import re, os
import pickle
import zlib
from datetime import timedelta, datetime


class DiskCache:
    def __init__(self, cache_dir='cache', max_length=255, expires=timedelta(seconds=30)):
        self.cache_dir = cache_dir
        self.max_length = max_length
        self.expires = expires

    def __getitem__(self, url):
        """Load data from disk for this URL"""
        path = self._url_to_path(url)
        if os.path.exists(path):
            with open(path, 'rb') as fp:
                result, timestamp = pickle.loads(zlib.decompress(fp.read()))
                if self._has_expired(timestamp):
                    raise KeyError(url + ' has expired')
                return result
        else:
            # URL has not yet been cached
            raise KeyError(url + ' does not exist')

    def __setitem__(self, url, result):
        """Save data to disk for this url"""
        path = self._url_to_path(url)
        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder)
        timestamp = datetime.utcnow()
        data = pickle.dumps((result, timestamp))
        with open(path, "wb") as fp:
            fp.write(zlib.compress(data))

    def _url_to_path(self, url):
        """Create file system path to this url"""
        components = urlparse.urlsplit(url)

        # Append index.html to empty paths
        path = components.path
        if not path:
            path = '/index.html'
        elif path.endswith('/'):
            path += 'index.html'

        filename = components.netloc + path + components.query

        # replace invalid characters
        filename = re.sub('[^/0-9a-zA-Z\-.,;_]', '_', filename)

        # Hash file name to avoid duplicate filename
        hash_value = hashlib.md5(filename.split("/")[-1]).hexdigest()
        filename = '/'.join(seg[:255] for seg in filename.split('/')[:-1]) + '/' + hash_value

        return os.path.join(self.cache_dir, filename)

    def _has_expired(self, timestamp):
        """Return whether this time stamp has expired"""
        return datetime.utcnow() > timestamp + self.expires
