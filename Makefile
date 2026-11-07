EPYDOC=sphinx-build
DSTDOC=$(SRCDOC)/html
SRCDOC=docs

all:
	python -m build -nw

install: all
	pip install .

uninstall:
	pip uninstall pyinotify

doc: clean-doc
# Must be installed before generating documentation
	pip show pyinotify >/dev/null 2>&1 || $(MAKE) install
	$(EPYDOC) $(SRCDOC) $(DSTDOC) || python -m pydoc -w pyinotify

clean-doc:
	rm -rf $(DSTDOC)
	rm -f pyinotify.html

clean: clean-doc
	find . \( -name '*~' -o \
		-name '*.pyc' -o \
		-name '*.pyo' \) \
		-print -exec rm {} \;
	rm -rf build dist pyinotify.egg-info
