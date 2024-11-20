build:
	cd cffi && python builder.py

run-only:
	python test.py

run: build run-only