EPYDOC=sphinx-build
DSTDOC=$(SRCDOC)/html
SRCDOC=docs

all:
	if test "$$(uname -s)" = "OpenBSD"; then export LDFLAGS="$${LDFLAGS} -L$${LOCALBASE:-/usr/local}/lib/inotify/ -linotify"; fi; \
	python -m build -nw

install: all
	pip install . $(INSTALL_ARGS)

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

deps:
	python3 -m ensurepip
	python3 -m pip install build setuptools

test: install
	python3 python3/pyinotify.py --version
	pyinotify --version
	python3 -m pyinotify --version
	mkdir -p /tmp
# Hangs in OpenBSD; OpenBSD users will have to investigate why.
	if test "$$(uname)" != "OpenBSD"; then python3 python3/examples/asyncio_notifier.py & fi
	sleep 5
	touch /tmp/foo
	rm -f /tmp/foo
