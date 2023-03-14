# Same as v2 except we set stream=True to not read the response body, which
# should leak sockets over time, but doesn't really seem to.

# This will SIGSEGV pmproxy occasionally.
# Rarely it will cause pmproxy to lock up.
# This didn't really uncover any interesting new behavior.

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

        r = session.get("{}{}/_fetch?names=kernel.all.nprocs".format(BASE, context), stream=True)
        print(tid, r.status_code)
        if r.status_code != 200:
            print(r.text)
            new = True
        time.sleep(random.uniform(2.0, 5.1))


for t in range(300):
    thread = threading.Thread(target=doit, args=[t])
    thread.start()
    time.sleep(1)
