dist: setup.py remindme
	cp README.md README.txt
	python setup.py sdist upload
	rm README.txt

clean: remindme/*pyc remindme/__pycache__
	sudo rm -r $^
