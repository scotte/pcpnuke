# Spawn 100 threads making pmproxy calls using a session per thread, sleep 1
# second between iterations and thread creation.
#
# This will SIGSEGV pmproxy often.
# Rarely it will cause pmproxy to lock up.

import requests
import threading
import time


HOST = "100.65.95.215"
BASE = "http://{}:7402/pmapi/".format(HOST)


def doit(tid):
    session = requests.Session()

    r = session.get("{}context".format(BASE))
    print(tid, r.status_code)
    if r.status_code != 200:
        print(r.text)

    j = r.json()
    context = j["context"]

    while True:
        r = session.get("{}{}/_fetch?names=kernel.all.nprocs".format(BASE, context))
        print(tid, r.status_code)
        if r.status_code != 200:
            print(r.text)
        time.sleep(1)


for t in range(100):
    thread = threading.Thread(target=doit, args=[t])
    thread.start()
    time.sleep(1)
