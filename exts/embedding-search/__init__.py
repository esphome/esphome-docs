import sphinx.search
import docutils.nodes
import os
import requests
import re
import json
import hashlib
from dotenv import load_dotenv
from os.path import dirname
from sphinx.jinja2glue import SphinxFileSystemLoader
from pathlib import Path


load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")
is_production = os.getenv("NETLIFY") == "true"

EXCLUDED_FILES = [
    "index.rst",
    "changelog/index.rst",
    "components/index.rst",
    "cookbook/index.rst",
    "custom/index.rst",
    "devices/index.rst",
    "guides/index.rst",
    "images/index.rst",
    "guides/supporters.rst",
    "guides/changelog.rst",
    "components/sensor/xiaomi_hhccjcy01.rst",
    "components/sensor/xiaomi_lywsdcgq.rst",
]
embedding_cache = {}
try:
    embedding_cache = json.load(open(Path("embedding_cache.json")))
except FileNotFoundError:
    pass

# char_count = 0


class IndexBuilder:
    _articles = {}
    _embeddings = {}

    def __init__(self, env, lang, options, scoring):
        ...

    def load(self, stream, format):
        frozen = format.load(stream)
        if not isinstance(frozen, dict):
            raise ValueError("old format")
        self._embeddings = frozen["embeddings"]

    def dump(self, stream, format):
        format.dump(self.freeze(), stream)

    def freeze(self):
        pending_embeddings = []
        for docname, article in self._articles.items():
            if article["hash"] in embedding_cache:
                self._embeddings[docname] = {
                    "title": article["title"],
                    "embedding": embedding_cache[article["hash"]],
                }
            else:
                pending_embeddings.append(docname)
        if len(pending_embeddings) > 0:
            print(
                f"getting embeddings from openai on {len(pending_embeddings)} documents..."
            )
            resp = requests.post(
                "https://api.openai.com/v1/embeddings",
                headers={
                    "Authorization": f"Bearer {OPENAI_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "input": [
                        self._articles[docname]["text"]
                        for docname in pending_embeddings
                    ],
                    "model": "text-embedding-ada-002",
                },
            ).json()
            for i, docname in enumerate(pending_embeddings):
                article = self._articles[docname]
                embedding_cache[article["hash"]] = resp["data"][i]["embedding"]
                self._embeddings[docname] = {
                    "title": article["title"],
                    "embedding": resp["data"][i]["embedding"],
                }
            json.dump(embedding_cache, open("embedding_cache.json", "w"))
        return {"embeddings": self._embeddings}

    def prune(self, docnames):
        self._articles = {
            docname: self._articles[docname]
            for docname in docnames
            if docname in self._articles
        }
        self._embeddings = {
            docname: self._embeddings[docname]
            for docname in docnames
            if docname in self._embeddings
        }

    def feed(self, docname, filename, title, doctree: docutils.nodes.document):
        # global char_count
        if filename in EXCLUDED_FILES:
            return
        with open(Path(__file__).parent.parent.parent / filename) as file:
            contents = file.read()
        text = contents.split(".. code-block")[0].split(".. figure")[0]

        first_subheader = None
        main_node = doctree.children[-1]
        if isinstance(main_node, docutils.nodes.section):
            has_text = False
            for child in main_node.children:
                if isinstance(child, docutils.nodes.paragraph):
                    has_text = True
                if isinstance(child, docutils.nodes.section):
                    if not has_text:
                        has_text = True
                        continue
                    first_node = child.children[0]
                    if isinstance(first_node, docutils.nodes.title):
                        first_subheader = first_node.astext()
                        break
        if first_subheader:
            text = contents.split("\n" + first_subheader + "\n")[0]

        text = re.sub(r"\n+", "\n", text).strip()
        text = text[:1024]
        # char_count += len(text)
        # print("characters:", char_count)

        self._articles[docname] = {
            "title": title,
            "text": text,
            "hash": hashlib.md5(text.encode("utf-8")).hexdigest(),
        }

    def label(self):
        return "searchindex.js"

    def get_js_stemmer_rawcodes(self):
        return []

    def context_for_searchtool(self):
        return {}


def builder_inited(app):
    app.builder.templates.loaders.insert(0, SphinxFileSystemLoader(dirname(__file__)))


def setup(app):
    app.connect("builder-inited", builder_inited)
    sphinx.search.IndexBuilder = IndexBuilder
    return {
        "version": "1.0.0",
        "parallel_read_safe": True,
        "parallel_write_safe": not is_production,
    }
