ESPHOME_PATH = ../esphome
ESPHOME_REF = v1.13.6

.PHONY: html html-strict cleanhtml deploy help webserver Makefile netlify netlify-api api netlify-dependencies svg2png copy-svg2png

html:
	sphinx-build -M html . _build -j auto -n $(O)

html-strict:
	sphinx-build -M html . _build -W -j auto -n $(O)

cleanhtml:
	rm -rf "_build/html/*"

svg2png:
	python3 svg2png.py

help:
	sphinx-build -M help . _build $(O)

api:
	mkdir -p _build/html/api
	@if [ ! -d "$(ESPHOME_PATH)" ]; then \
	  git clone --branch $(ESPHOME_REF) https://github.com/esphome/esphome.git $(ESPHOME_PATH); \
	fi
	ESPHOME_PATH=$(ESPHOME_PATH) doxygen Doxygen

netlify-api: netlify-dependencies
	mkdir -p _build/html/api
	@if [ ! -d "$(ESPHOME_PATH)" ]; then \
	  git clone --branch $(ESPHOME_REF) https://github.com/esphome/esphome.git $(ESPHOME_PATH); \
	fi
	ESPHOME_PATH=$(ESPHOME_PATH) ../doxybin/doxygen Doxygen

netlify-dependencies:
	mkdir -p ../doxybin
	curl -L https://github.com/esphome/esphome-docs/releases/download/v1.10.1/doxygen-1.8.13.xz | xz -d >../doxybin/doxygen
	chmod +x ../doxybin/doxygen

copy-svg2png:
	cp svg2png/*.png _build/html/_images/

netlify: netlify-dependencies netlify-api html copy-svg2png

webserver: html
	cd "_build/html" && python3 -m http.server

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	sphinx-build -M $@ . _build $(O)
