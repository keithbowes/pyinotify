EPYDOC=sphinx-build
DSTDOC=python3/docs/html
SRCDOC=docs

all: doc
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
	python3 -m pip install build setuptools Sphinx

# Make sure that it works when opened in the interpreter, when called in the
# path, when called as a module, and that the API can detect file changes.
test: install
	python3 python3/pyinotify.py --version
	pyinotify --version
	python3 -m pyinotify --version
	mkdir -p $${TMPDIR:-/tmp}
	TEST=1 python3 python3/examples/threaded_notifier.py &
	i=0; \
	while ! test -e $${TMPDIR:-/tmp}/.notifier_started && test $$i -lt 60; do i=`expr $$i + 1`; sleep 1; done;
	touch $${TMPDIR:-/tmp}/foo
	mv $${TMPDIR:-/tmp}/foo $${TMPDIR:-/tmp}/bar
	rm -f $${TMPDIR:-/tmp}/bar
	i=0; \
	while ! test -e $${TMPDIR:-/tmp}/.notifier_finished && test $$i -lt 60; do i=`expr $$i + 1`; sleep 1; done;
	rm -f $${TMPDIR:-/tmp}/.notifier_finished
	rm -f $${TMPDIR:-/tmp}/.notifier_started
