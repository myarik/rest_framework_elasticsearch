.PHONY: help

.DEFAULT_GOAL := help


help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build developer containers.
	docker-compose  build

shell: ## Run bash shell
	docker-compose  run --rm python sh

pytest: # Run unit testing, pytest.
	docker-compose  run --rm python pytest

tox: # Run all tox test options
	docker-compose  run --rm python tox

tox_latest: # Run all tox test with modern packages (python 3)
	docker-compose  run --rm python tox -e drf{310,311}-py{36,38}-dj{200,300}-esdsl{6,7}

tox_medium: # Run all tox test with medium packages (python 3)
	docker-compose  run --rm python tox -e drf{37,36}-py{36,38}-dj111-esdsl{6,7}

tox_oldest: # Run all tox test with old packages (python 2)
	docker-compose  run --rm python tox -e drf{35,36}-py{27,36,38}-dj{108,109,111}-esdsl{6,7}



