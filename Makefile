SHELL := /bin/bash
PYTHON := $(shell source ~/.bashrc && pyenv which python)

export PYTHONPATH := $(PWD)

setup: compile-libyang
	pyenv install 3.13.0
	pyenv virtualenv 3.13.0 libyang-cffi-playground
	pyenv local libyang-cffi-playground
	pip install -r extra/requirements.txt

compile-libyang:
	extra/build_libyang.sh

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