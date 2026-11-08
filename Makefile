EPYDOC=sphinx-build
DSTDOC=$(SRCDOC)/html
SRCDOC=docs

all:
	if test "$$(uname -s)" = "OpenBSD"; then export LDFLAGS="$${LDFLAGS} -L$${LOCALBASE}/lib/inotify/ -linotify"; fi; \
	python -m build -nw

install: all
	pip install .

uninstall:
	pip uninstall pyinotify

doc: clean-doc
	$(EPYDOC) $(SRCDOC) $(DSTDOC) || python -m pydoc -w python3/pyinotify.py

clean-doc:
	rm -rf $(DSTDOC)
	rm -f pyinotify.html

clean: clean-doc
	find . \( -name '*~' -o \
		-name '*.pyc' -o \
		-name '*.pyo' \) \
		-print -exec rm {} \;
	rm -rf build dist pyinotify.egg-info
