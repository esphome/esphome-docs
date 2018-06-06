# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = esphomelib
SOURCEDIR     = .
BUILDDIR      = _build
ESPHOMELIB_PATH = ../esphomelib

.PHONY: html cleanhtml minifyhtml doxyg cleandoxyg copypdf fixdeploy releasedeploy help webserver Makefile

html: _doxyxml
	$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

cleanhtml: cleandoxy
	rm -rf "$(BUILDDIR)/html/*"

minifyhtml: html
	./minify.sh

doxyg: cleandoxyg _doxyxml

cleandoxyg:
	rm -rf _doxyxml

_doxyxml:
	ESPHOMELIB_PATH=$(ESPHOMELIB_PATH) doxygen Doxygen

copypdf:
	cp $(BUILDDIR)/latex/$(SPHINXPROJ).pdf $(BUILDDIR)/esphomelib.pdf

fixdeploy: copypdf cleanhtml doxyg html minifyhtml
	touch "$(BUILDDIR)/html/.nojekyll"
	echo "esphomelib.com" >"$(BUILDDIR)/html/CNAME"
	cp $(BUILDDIR)/esphomelib.pdf $(BUILDDIR)/latex/$(SPHINXPROJ).pdf
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

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
