dist: setup.py remindme
	python setup.py sdist

upload: sdist
	python setup.py upload

clean: remindme/*pyc remindme/__pycache__
	sudo rm -r $^
