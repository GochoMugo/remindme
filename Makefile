.PHONY: deps test shell-tests clean

# create and upload a distribution (for releases)
dist: setup.py remindme/
	cp README.md README.txt
	python setup.py sdist upload
	rm README.txt
	@echo 'Dist built and uploaded...'

# install dependencies
deps:
	pip install -r requirements.txt

# run tests (uses the default python interpreter)
test:
	python -m test

# run tests against different python versions
PYTHON_SHELLS = python2.6 python2.7 python3 python3.2
shell-tests:
	@for shell in $(PYTHON_SHELLS); \
	do \
		echo ''; \
		echo '\nRunning Tests in ' $$shell; \
		$$shell -m test; \
	done

# clean directory of unnecessary files
clean:
	@- rm -rf remindme/*.pyc remindme/__pycache__ .remindme
	@ rm -rf dist/ MANIFEST remindme.egg-info build/
	@ rm -rf test/_test* test/*.pyc
	@echo 'Cleaned...'
