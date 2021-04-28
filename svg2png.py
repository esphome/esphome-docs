from pathlib import Path
import re
import shlex
import subprocess
import threading
import queue
import sys


to_p = Path("svg2png")
to_p.mkdir(exist_ok=True)
for f in to_p.glob("*.png"):
    f.unlink()

images = [
    f
    for f in Path("_build/html/_images/").glob("*.svg")
    if not re.match(r"^seg[0-9A-F]{2}$", f.stem)
]
q = queue.Queue()


def worker():
    while True:
        item = q.get()
        if item is None:
            break

        to = to_p / item.with_suffix(".png").name
        args = [
            "inkscape",
            "-z",
            "-e",
            str(to.absolute()),
            "-w",
            "800",
            "-background",
            "white",
            str(item.absolute()),
        ]
        print("Running:  {}".format(" ".join(shlex.quote(x) for x in args)))
        proc = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if b"Bitmap saved as" not in proc.stdout:
            print("Error!")
            print(proc.stdout)
            sys.exit(1)

        q.task_done()


NUM_THREADS = 8
threads = []
for i in range(NUM_THREADS):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

for img in sorted(images):
    q.put(img)

q.join()

for i in range(NUM_THREADS):
    q.put(None)
for t in threads:
    t.join()
