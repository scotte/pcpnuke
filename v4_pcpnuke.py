# Same as v2 except it uses /fetch?name= instead of /_fetch?names= and
# on each iteration it requests a number of metrics via individual calls
# (because this is what the real client does)

# This will SIGSEGV pmproxy regularly, and I saw one SIGABRT.

import random
import requests
import threading
import time


HOST = "100.65.95.215"
BASE = "http://{}:7402/pmapi/".format(HOST)
PMDS = ["disk.dev.util",
        "kernel.cpu.util.idle",
        "kernel.cpu.util.intr",
        "kernel.cpu.util.nice",
        "kernel.cpu.util.steal",
        "kernel.cpu.util.sys",
        "kernel.cpu.util.user",
        "kernel.cpu.util.wait",
        "network.interface.in.bytes",
        "network.interface.out.bytes"]


def connect(tid):
    session = requests.Session()

    r = session.get("{}context".format(BASE))
    print(r.status_code)
    if r.status_code != 200:
        print(r.text)

    j = r.json()
    context = j["context"]
    return (session, context)


def doit(tid):
    while True:
        (session, context) = connect(tid)

        for pmd in PMDS:
            r = session.get("{}{}/fetch?name={}".format(BASE, context, pmd))
            # print(tid, r.status_code)
            if r.status_code != 200:
                print(r.text)
                (session, context) = connect(tid)
        time.sleep(random.uniform(2.0, 5.1))


for t in range(100):
    thread = threading.Thread(target=doit, args=[t])
    thread.start()
    time.sleep(1)
