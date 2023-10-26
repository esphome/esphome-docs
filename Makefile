ESPHOME_PATH = ../esphome
ESPHOME_REF = 2023.10.3

.PHONY: html html-strict cleanhtml deploy help live-html live-pagefind Makefile netlify netlify-api api netlify-dependencies svg2png copy-svg2png minify

html:
	sphinx-build -M html . _build -j auto -n $(O)
	pagefind

live-html:	html
	sphinx-autobuild . _build -j auto -n $(O) --host 0.0.0.0

live-pagefind:	html
	pagefind --serve

html-strict:
	sphinx-build -M html . _build -W -j auto -n $(O)
	pagefind

minify:
	minify _static/webserver-v1.js > _static/webserver-v1.min.js
	minify _static/webserver-v1.css > _static/webserver-v1.min.css

cleanhtml:
	rm -rf "_build/html/*"

svg2png:
	python3 svg2png.py

help:
	sphinx-build -M help . _build $(O)

api:
	mkdir -p _build/html/api
	@if [ ! -d "$(ESPHOME_PATH)" ]; then \
	  git clone --branch $(ESPHOME_REF) https://github.com/esphome/esphome.git $(ESPHOME_PATH) || \
	  git clone --branch beta https://github.com/esphome/esphome.git $(ESPHOME_PATH); \
	fi
	ESPHOME_PATH=$(ESPHOME_PATH) doxygen Doxygen

netlify-api: netlify-dependencies
	mkdir -p _build/html/api
	@if [ ! -d "$(ESPHOME_PATH)" ]; then \
	  git clone --branch $(ESPHOME_REF) https://github.com/esphome/esphome.git $(ESPHOME_PATH) || \
	  git clone --branch beta https://github.com/esphome/esphome.git $(ESPHOME_PATH); \
	fi
	ESPHOME_PATH=$(ESPHOME_PATH) ../doxybin/doxygen Doxygen

netlify-dependencies: pagefind-binary
	mkdir -p ../doxybin
	curl -L https://github.com/esphome/esphome-docs/releases/download/v1.10.1/doxygen-1.8.13.xz | xz -d >../doxybin/doxygen
	chmod +x ../doxybin/doxygen

pagefind-binary:
	mkdir -p ../pagefindbin
	curl -o pagefind-v1.0.2-x86_64-unknown-linux-musl.tar.gz https://github.com/CloudCannon/pagefind/releases/download/v1.0.2/pagefind-v1.0.2-x86_64-unknown-linux-musl.tar.gz -L
	tar xzf pagefind-v1.0.2-x86_64-unknown-linux-musl.tar.gz
	rm pagefind-v1.0.2-x86_64-unknown-linux-musl.tar.gz
	mv pagefind ../pagefindbin


copy-svg2png:
	cp svg2png/*.png _build/html/_images/

netlify: netlify-dependencies netlify-api html copy-svg2png

lint: html-strict
	python3 lint.py

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	sphinx-build -M $@ . _build $(O)
