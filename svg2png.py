from pathlib import Path
import re
import shlex
import subprocess


to_p = Path('svg2png')
to_p.mkdir(exist_ok=True)
for f in to_p.glob('*.png'):
    f.unlink()

images = [f for f in Path('_build/html/_images/').glob('*.svg')
          if not re.match(r'^seg[0-9A-F]{2}$', f.stem)]

for from_ in sorted(images):
    to_ = to_p / from_.with_suffix('.png').name
    args = ['inkscape', '-z', '-e', str(to_.absolute()), '-w', '800',
            '-background', 'white', str(from_.absolute())]
    print("Running:  {}".format(' '.join(shlex.quote(x) for x in args)))
    proc = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if b'Bitmap saved as' not in proc.stdout:
        print("Error!")
        print(proc.stdout)
        raise ValueError
