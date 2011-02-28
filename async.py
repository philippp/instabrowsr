import urllib
from threading import Thread
from Queue import Queue

NUM_WORKERS = 20

class Dnld:
    def __init__(self):
        self.Q = Queue()
        for i in xrange(NUM_WORKERS):
            t = Thread(target=self.worker)
            t.setDaemon(True)
            t.start()

    def worker(self):
        while 1:
            url, Q = self.Q.get()
            try:
                f = urllib.urlopen(url)
                Q.put(('ok', url, f.read()))
                f.close()
            except Exception, e:
                Q.put(('error', url, e))
                try: f.close() # clean up
                except: pass

    def download_urls(self, urls):
        if not isinstance(urls, (list,tuple)): urls=[urls]
        Q = Queue() # Create a second queue so the worker 
                    # threads can send the data back again
        for url in urls:
            # Add the URLs in `L` to be downloaded asynchronously
            self.Q.put((url, Q))

        rtn = []
        for i in xrange(len(urls)):
            # Get the data as it arrives, raising 
            # any exceptions if they occur
            status, url, data = Q.get()
            if status == 'ok':
                rtn.append((url, data))
            else:
                print "status=%s data=%s" % (status,data)
        return rtn

