dist: setup.py remindme
	cp README.md README.txt
	python setup.py sdist upload
	rm README.txt
	@echo 'Dist build and uploaded...'

clean:
	@sudo rm -r remindme/*pyc remindme/__pycache__ .remindme
	@echo 'Cleaned...'
