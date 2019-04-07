ESPHOME_CORE_PATH = ../esphome-core
ESPHOME_CORE_TAG = v1.12.1

.PHONY: html cleanhtml deploy help webserver Makefile netlify netlify-api api netlify-dependencies svg2png copy-svg2png

html:
	sphinx-build -M html . _build -W $(O)

cleanhtml:
	rm -rf "_build/html/*"

svg2png:
	python3 svg2png.py

help:
	sphinx-build -M help . _build $(O)

api:
	mkdir -p _build/html/api
	@if [ ! -d "$(ESPHOME_CORE_PATH)" ]; then \
	  git clone --branch $(ESPHOME_CORE_TAG) https://github.com/esphome/esphome-core.git $(ESPHOME_CORE_PATH); \
	fi
	ESPHOME_CORE_PATH=$(ESPHOME_CORE_PATH) doxygen Doxygen

netlify-api: netlify-dependencies
	mkdir -p _build/html/api
	@if [ ! -d "$(ESPHOME_CORE_PATH)" ]; then \
	  git clone --branch $(ESPHOME_CORE_TAG) https://github.com/esphome/esphome-core.git $(ESPHOME_CORE_PATH); \
	fi
	ESPHOME_CORE_PATH=$(ESPHOME_CORE_PATH) ../doxybin/doxygen Doxygen

netlify-dependencies:
	mkdir -p ../doxybin
	curl -L https://github.com/esphome/esphome-docs/releases/download/v1.10.1/doxygen-1.8.13.xz | xz -d >../doxybin/doxygen
	chmod +x ../doxybin/doxygen

copy-svg2png:
	cp svg2png/*.png _build/html/_images/

netlify: netlify-dependencies netlify-api html copy-svg2png
	python3 travis.py

webserver: html
	cd "_build/html" && python3 -m http.server

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	sphinx-build -M $@ . _build $(O)
