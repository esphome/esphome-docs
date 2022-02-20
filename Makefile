.PHONY: html html-strict cleanhtml deploy help live-html Makefile netlify svg2png copy-svg2png minify

html:
	sphinx-build -M html . _build -j auto -n $(O)
live-html:
	sphinx-autobuild . _build -j auto -n $(O) --host 0.0.0.0

html-strict:
	sphinx-build -M html . _build -W -j auto -n $(O)

minify:
	minify _static/webserver-v1.js > _static/webserver-v1.min.js
	minify _static/webserver-v1.css > _static/webserver-v1.min.css

cleanhtml:
	rm -rf "_build/html/*"

svg2png:
	python3 svg2png.py

help:
	sphinx-build -M help . _build $(O)

copy-svg2png:
	cp svg2png/*.png _build/html/_images/

netlify: html copy-svg2png

lint: html-strict
	python3 lint.py

linkcheck: html
	sphinx-build -M linkcheck . _build

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	sphinx-build -M $@ . _build $(O)
