.PHONY: all docs

all: anythingdb

docs:
	# Use README in the documentation, removing selected lines before
	cp README.md docs/readme.md
	sed -i '/-- NODOC --/d' ./docs/readme.md
	rm -f docs/readme.rst
	m2r docs/readme.md
	rm docs/readme.md

	# Update requirements.txt
	poetry export --without-hashes --with docs --format=requirements.txt > docs/requirements.txt

	cd docs && make clean && make html
