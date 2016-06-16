static:
	npm --prefix admin/static run build:js

static-watch:
	npm --prefix admin/static run watch:js

static-test:
	npm --prefix admin/static run test:js

test:
	PYTHONPATH=third-party nosetests tests

lint:
	PYTHONPATH=third-party pylint ikcms admin ws_admin models tests
