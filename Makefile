all:
	$(error please pick a target)

install:
	# Create venv directory if not exist
	test -d venv || virtualenv venv
	./venv/bin/python -m pip install -r requirements.txt

dev-env: install
	./venv/bin/python -m pip install -r requirements-dev.txt

dev-build: dev-env
	find . -name '*.pyc' -exec rm -f {} \;
	./venv/bin/pyflakes json_log_parser tests
	./venv/bin/pytest \
		--pep8 \
		--disable-warnings \
		--verbose \
	    json_log_parser tests

test: dev-build
	./venv/bin/pytest \
	    --doctest-modules \
	    --disable-warnings \
	    --verbose \
	    json_log_parser tests

coverage: dev-build
	./venv/bin/pytest \
		--cov-report html:cov_html \
		--cov-report term \
		--cov json_log_parser/

package:
	python setup.py sdist

clean:
	rm -rf build dist json_log_parser.egg-info
