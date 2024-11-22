compile-libyang:
	./build_libyang.sh

build:
	cd cffi && python builder.py

run-only:
	python test.py

run: build run-only

run-test-bindings: build
	python cffi/test_own_bindings.py
