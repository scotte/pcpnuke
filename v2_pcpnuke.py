# Spawn 300 threads make pmproxy calls using a session per thread, sleep
# a random amount between 2 and 5.1 seconds (so we hit an occasional context
# time out) between iterations and spawn threads every 1 second. If the
# fetch returns non 200 (such as context expiration), then create a new context
# in a new session.
#
# This will SIGSEGV pmproxy occasionally.

import random
import requests
import threading
import time


HOST = "100.65.95.215"
BASE = "http://{}:7402/pmapi/".format(HOST)


def doit(tid):
    new = True
    while True:
        if new:
            session = requests.Session()

            r = session.get("{}context".format(BASE))
            print(tid, r.status_code)
            if r.status_code != 200:
                print(r.text)

            j = r.json()
            context = j["context"]
            new = False

        r = session.get("{}{}/_fetch?names=kernel.all.nprocs".format(BASE, context))
        print(tid, r.status_code)
        if r.status_code != 200:
            print(r.text)
            new = True
        time.sleep(random.uniform(2.0, 5.1))


for t in range(300):
    thread = threading.Thread(target=doit, args=[t])
    thread.start()
    time.sleep(1)
