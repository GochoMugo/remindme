html:
	@make prepare > /dev/null
	@python raw/prepare.py
	@jade raw/ --out . \
		--path includes/ \
		--obj out.json \
		--pretty

files = installation.html usage.html contribution.html issues.html license.html
prepare:
	[ -d includes ] || mkdir includes
	touch $(files)
	mv --no-clobber $(files) includes/
	rm $(files)

clean:
	rm out.json

.PHONY: html prepare clean
