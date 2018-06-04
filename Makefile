# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = esphomelib
SOURCEDIR     = .
BUILDDIR      = _build
ESPHOMELIB_PATH = ../esphomelib

html:
	$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

cleanhtml:
	rm -rf "$(BUILDDIR)/html/*" _doxyxml/

minifyhtml: html
	./minify.sh

doxyg:
	ESPHOMELIB_PATH=$(ESPHOMELIB_PATH) doxygen Doxygen

fixdeploy: cleanhtml doxyg html minifyhtml
	touch "$(BUILDDIR)/html/.nojekyll"
	echo "esphomelib.com" >"$(BUILDDIR)/html/CNAME"
	cd "$(BUILDDIR)/html" && git add --all && git commit -m "Deploy to gh-pages"
	@printf "Run \033[0;36mcd $(BUILDDIR)/html && git push origin gh-pages\033[0m to deploy\n"

releasedeploy: cleanhtml doxyg html minifyhtml
	touch "$(BUILDDIR)/html/.nojekyll"
	echo "esphomelib.com" >"$(BUILDDIR)/html/CNAME"
	-yes '' | make latexpdf
	cp $(BUILDDIR)/latex/$(SPHINXPROJ).pdf $(BUILDDIR)/html/_static/esphomelib.pdf
	cd "$(BUILDDIR)/html" && git add --all && git commit -m "Deploy to gh-pages"
	@printf "Run \033[0;36mcd $(BUILDDIR)/html && git push origin gh-pages\033[0m to deploy\n"

help:
	$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

webserver: html
	cd "$(BUILDDIR)/html" && python3 -m http.server

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
