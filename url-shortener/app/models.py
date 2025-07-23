import threading
import time

class ThreadSafeURLStore:
    def __init__(self):
        self.lock = threading.Lock()
        self.data = {}

    def create(self, short_code, url):
        with self.lock:
            self.data[short_code] = {
                'url': url,
                'clicks': 0,
                'created_at': time.strftime('%Y-%m-%dT%H:%M:%S')
            }

    def exists(self, short_code):
        with self.lock:
            return short_code in self.data

    def get_url(self, short_code):
        with self.lock:
            entry = self.data.get(short_code)
            return entry['url'] if entry else None

    def increment_click(self, short_code):
        with self.lock:
            if short_code in self.data:
                self.data[short_code]['clicks'] += 1

    def get_metadata(self, short_code):
        with self.lock:
            entry = self.data.get(short_code)
            if entry is None:
                return None
            return {
                'url': entry['url'],
                'clicks': entry['clicks'],
                'created_at': entry['created_at']
            }

url_store = ThreadSafeURLStore()
