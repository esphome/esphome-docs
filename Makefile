# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = esphomelib
SOURCEDIR     = .
BUILDDIR      = _build
ESPHOMELIB_PATH = ../esphomelib
ESPHOMELIB_TAG = v1.10.0

.PHONY: html cleanhtml doxyg cleandoxyg deploy help webserver Makefile $(ESPHOMELIB_PATH)

html: _doxyxml
	$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

cleanhtml: cleandoxyg
	rm -rf "$(BUILDDIR)/html/*"

doxyg: cleandoxyg _doxyxml

cleandoxyg:
	rm -rf _doxyxml

_doxyxml:
	ESPHOMELIB_PATH=$(ESPHOMELIB_PATH) doxygen Doxygen

$(ESPHOMELIB_PATH):
	@if [ ! -d "$(ESPHOMELIB_PATH)" ]; then \
	  git clone --branch $(ESPHOMELIB_TAG) https://github.com/OttoWinter/esphomelib.git $(ESPHOMELIB_PATH); \
	fi

convertimages:
	python3 svg2png.py

help:
	$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

webserver: html
	cd "$(BUILDDIR)/html" && python3 -m http.server

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
