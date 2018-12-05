import os

def create_nojekyll(app, env):
    if app.builder.format == 'html':
        path = os.path.join(app.builder.outdir, '.nojekyll')
        open(path, 'wt').close()

        path = os.path.join(app.builder.outdir, 'CNAME')
        with open(path, 'wt') as f:
            f.write(os.getenv('CNAME', 'esphomelib.com'))


def setup(app):
    app.connect('env-updated', create_nojekyll)
