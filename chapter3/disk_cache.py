import urlparse
import hashlib
import re, os


class DiskCache:
    def __init__(self, cache_dir='cache', max_length=255):
        self.cache_dir = cache_dir
        self.max_length = max_length

    def url_to_path(self, url):
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
