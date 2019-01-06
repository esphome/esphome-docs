import os

def create_nojekyll(app, env):
    if app.builder.format == 'html':
        path = os.path.join(app.builder.outdir, '.nojekyll')
        open(path, 'wt').close()

        path = os.path.join(app.builder.outdir, 'CNAME')
        with open(path, 'wt') as f:
            f.write(app.env.config.cname)


def setup(app):
    app.add_config_value('cname', 'esphomelib.com', 'html')
    app.connect('env-updated', create_nojekyll)
