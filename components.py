import os
import json



def setup(app):
    """Setup connects events to the components output builder"""
    app.connect("html-page-context", add_component_details)
    app.connect("build-finished", create_output)
    app.compoents_output = {}

    is_production = os.getenv("PRODUCTION") == "YES"

    return {
        "version": "1.0.0",
        "parallel_read_safe": True,
        "parallel_write_safe": not is_production,
    }


def add_component_details(app, pagename, templatename, context, doctree):
    """As each page is built, collect page details for the output."""
    if pagename.startswith("components/"):
        app.compoents_output[pagename] = {
            "title": context["title"],
            "url": context["pageurl"]
        }


def create_output(app, exception):
    """Generates the components.json from the collected component pages"""
    with open(os.path.join(app.builder.outdir, "components.json"), "wt") as f:
        f.write(json.dumps(app.compoents_output))
