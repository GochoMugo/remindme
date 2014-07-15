.PHONY: tests, clean

dist: setup.py remindme
	cp README.md README.txt
	python setup.py sdist upload
	rm README.txt
	@echo 'Dist build and uploaded...'

PYTHON_SHELLS = python2.6 python2.7 python3 python3.2
tests:
	@for shell in $(PYTHON_SHELLS); \
	do \
		echo ''; \
		echo '\nRunning Tests in ' $$shell; \
		$$shell tests.py; \
	done

clean:
	- sudo rm -r remindme/*pyc remindme/__pycache__ .remindme
	@echo 'Cleaned...'
