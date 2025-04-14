SHELL := /bin/bash
PYTHON := $(shell source ~/.bashrc && pyenv which python)
PYTHON_VERSION = 3.13.0

export PYTHONPATH := $(PWD)

check-python:
	@if pyenv versions | grep -q $(PYTHON_VERSION); then \
		echo "Python $(PYTHON_VERSION) is already installed."; \
	else \
		pyenv install $(PYTHON_VERSION); \
	fi

setup: compile-libraries check-python
	pyenv virtualenv $(PYTHON_VERSION) libyang-cffi-playground
	pyenv local libyang-cffi-playground
	pip install -r extra/requirements.txt

compile-libraries:  # libyang and cJSON
	extra/build_libraries.sh

build:
	cd bindings && python builder.py

run-mixed-libyang-with-bindings: build
	python extra/debug_mixed_libyang_python.py

run-custom-bindings: build
	python use_custom_bindings.py

benchmark: build
	python tests/benchmarks.py

valgrind: build
	PYTHONMALLOC=malloc valgrind --leak-check=full --show-leak-kinds=all $(PYTHON) use_custom_bindings.py

test: build
	pytest -s -vv tests/*