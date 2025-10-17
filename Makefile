PYTHON_VERSION = 3.13.0

ifdef USE_SYSTEM_PYTHON
PYTHON := $(shell which python)
else
PYTHON := $(shell pyenv which python)
endif

export PYTHONPATH := $(PWD)

check-python:
	@if pyenv versions | grep -q $(PYTHON_VERSION); then \
		echo "Python $(PYTHON_VERSION) is already installed."; \
	else \
		pyenv install $(PYTHON_VERSION); \
	fi

configure-pyenv:
	pyenv virtualenv $(PYTHON_VERSION) libyang-bindings
	pyenv local libyang-bindings
	pip install -r extra/requirements.txt

setup: compile-libraries check-python configure-pyenv

compile-libraries:  # libyang and cJSON
	extra/build_libraries.sh

build:
	cd bindings && python builder.py

docker-build:
	docker build -t libyang-bindings .

docker-run:
	docker run -it -e USE_SYSTEM_PYTHON=1 libyang-bindings /bin/bash

run-mixed-libyang-with-bindings: build
	python extra/debug_mixed_libyang_python.py

run-custom-bindings: build
	python use_custom_bindings.py

benchmark: build
	python tests/benchmarks.py

valgrind: build
	PYTHONMALLOC=malloc valgrind --leak-check=full --show-leak-kinds=all $(PYTHON) use_custom_bindings.py

test: build
	pytest -s -vv tests/unit_tests.py
