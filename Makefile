js:
	npm --prefix admin/static run build:js


js-watch:
	npm --prefix admin/static run watch:js


test-js:
	npm --prefix admin/static run test:js

test-py:
	PYTHONPATH=third-party nosetests tests