PYTHON := $(shell pyenv which python)

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
	python bindings/debug_mixed_libyang_python.py

run-custom-bindings: build
	python bindings/use_custom_bindings.py

valgrind: build
	PYTHONMALLOC=malloc valgrind --leak-check=full --show-leak-kinds=all $(PYTHON) bindings/use_custom_bindings.py
