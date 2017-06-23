from datetime import datetime, timedelta
from pymongo import MongoClient,errors

class MongoQueue:
    # Possible states of a download
    OUTSTANDING, PROCESSING, COMPLETE = range(3)

    def __init__(self, client=None, timeout=300):
        self.client = MongoClient('localhost', 27017) if client is None else client
        self.timeout = timeout
        self.db = self.client.cache

    def __nonzero__(self):
        """return True if there are more jobs to process"""
        record = self.db.crawl_queue.find_one(
            {'status': {'$ne': self.COMPLETE}}
        )
        return True if record else False

    def push(self, url):
        """Add new URL to queue if does not exist"""
        try:
            self.db.crawl_queue.insert({
                '_id': url, 'status': self.OUTSTANDING
            })
        except errors.DuplicateKeyError as e:
            # this is already in the queue
            pass

    def pop(self):
        """Get an outstanding URL from the queue and set its status to processing. If the queue is empty a KeyError
        exception is raised"""
        record = self.db.crawl_queue.find_and_modify(
            query={'status': self.OUTSTANDING},
            update={
                '$set': {
                    'status': self.PROCESSING,
                    'timestamp': datetime.now()
                }
            }
        )

        if record:
            return record['_id']
        else:
            self.repair()
            raise KeyError()

    def complete(self, url):
        self.db.crawl_queue.update({'_id': url}, {'$set': {'status': self.COMPLETE}})

    def repair(self):
        """Release stalled jobs"""
        record = self.db.crawl_queue.find_and_modify(
            query={
                'timestamp': {'lt': datetime.now() - timedelta(seconds=self.timeout)},
                'status': {'$ne': self.COMPLETE}
            },
            update={
                '$set':{'status': self.OUTSTANDING}
            }
        )
        if record:
            print("Released:", record["_id"])
