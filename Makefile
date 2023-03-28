.PHONY: all clean_models docs

all: anythingdb

anythingdb:
	datamodel-codegen  --input openapi/anythingdb.yaml --input-file-type openapi --output swx/models/anythingdb.py --base-class swx.models.basemodel.IterBaseModel
	python tools/clean_models.py swx/models/anythingdb.py

clean_models:
	python tools/clean_models.py swx/models/anythingdb.py

docs:
	# Use README in the documentation, removing selected lines before
	cp README.md docs/readme.md
	sed -i '/-- NODOC --/d' ./docs/readme.md
	rm docs/readme.rst
	m2r docs/readme.md
	rm docs/readme.md

	cd docs && make html
