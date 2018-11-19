import os
import shlex
import subprocess


path = '_build/html/_images/'

for from_ in os.listdir(path):
    if not from_.endswith('.svg'):
        continue

    to_ = from_[:-len('.svg')] + '.png'
    from_ = os.path.abspath(os.path.join(path, from_))
    to_ = os.path.abspath(os.path.join(path, to_))

    if os.path.exists(to_):
        to_mtime = os.path.getmtime(to_)
        from_mtime = os.path.getmtime(from_)
        if to_mtime > from_mtime:
            # Let's not re-convert files if we've already converted them
            # Yes, mtime is not great but it's better than having the builds take
            # ages
            continue

    args = ['inkscape', '-z', '-e', to_, '-w', '800',
            '-background', 'white', from_]
    print("Running:  {}".format(' '.join(shlex.quote(x) for x in args)))
    proc = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if b'Bitmap saved as' not in proc.stdout:
        print("Error!")
        print(proc.stdout)
