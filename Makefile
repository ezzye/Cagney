.PHONY: all setup clean zip test

ifeq (, $(shell which pipenv))
$(error "No pipenv in $(PATH), consider doing brew install pipenv")
endif

all: clean zip setup test

ZIP_DIR := $(shell pwd)

clean:
	rm -f piper.zip
	pipenv --rm || :

setup:
	pipenv sync -d
	bundle install --gemfile component-test/cucumber/Gemfile

zip:
	pipenv sync
	zip -qr9 piper.zip src/ -x *.pyc
	cd `pipenv --venv`/lib/python3.*/site-packages; zip -qr9 $(ZIP_DIR)/piper.zip .

unittest:
	pipenv run python -m unittest discover -v -s test

test:
	pipenv run python -m unittest discover -v -s test
	./component-test/cucumber/test
