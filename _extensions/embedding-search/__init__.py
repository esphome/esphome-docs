import os
from os.path import dirname, join
from json import dump
from sphinx.application import Sphinx
from sphinx.util.fileutil import copy_asset_file
from sphinx.jinja2glue import SphinxFileSystemLoader

from .embed import tokenize, embed

is_production = os.getenv("NETLIFY") == "true"

def builder_inited(app):
    app.builder.templates.loaders.insert(0, SphinxFileSystemLoader(dirname(__file__)))
    
def build_finished(app: Sphinx, exception):
    embedding_collection = []
    for page in app.env.titles:
        title = app.env.titles[page].astext()
        tokens = tokenize(title)
        embedding = embed(tokens)
        if embedding:
            embedding_collection.append({ "page": f"{page}.html", "title": title, "embedding": embedding})
    dump(embedding_collection, open(join(app.builder.outdir, "embedding-index.json"), "w"))

    output_path = join(app.builder.outdir, "_static")
    copy_asset_file(join(dirname(__file__), "glove-25d-reduced.txt"), output_path)
    copy_asset_file(join(dirname(__file__), "searchbox.js"), output_path)

def setup(app):
    app.connect("builder-inited", builder_inited)
    app.connect("build-finished", build_finished)
    return {
        "version": "1.0.0",
        "parallel_read_safe": True,
        "parallel_write_safe": not is_production,
    }
