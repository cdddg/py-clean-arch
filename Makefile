SETTINGS_PATH ?= ./pyproject.toml
PORT ?= 8000
GIT_ARGS := --name-only --diff-filter=d --cached
ifneq ($(DIFF_SRC),)
	GIT_ARGS := --name-only --diff-filter=d $(DIFF_SRC)...HEAD
endif

DIFF_FILES = `git diff $(GIT_ARGS)`
DIFF_PYTHONS = `git diff $(GIT_ARGS) | grep .py$$`


format:
	@if [[ ! -z "${DIFF_PYTHONS}" ]]; then \
		echo "> autoflake"; \
		autoflake --remove-all-unused-imports --ignore-init-module-imports -r -i $(DIFF_FILES); \
		echo "> isort"; \
		isort -settings_path=$(SETTINGS_PATH) --quiet $(DIFF_PYTHONS); \
		echo "> black"; \
		black --config $(SETTINGS_PATH) -q $(DIFF_PYTHONS); \
	fi

lint:
	@if command -v cspell > /dev/null; then \
		echo "> cspell"; cspell --gitignore --no-progress --no-summary --no-must-find-files $(DIFF_FILES); \
	fi;
	@if [[ ! -z "$(DIFF_PYTHONS)" ]]; then \
		echo "> pylint"; pylint --rcfile=$(SETTINGS_PATH) -sn $(DIFF_PYTHONS); \
		echo "> ruff"; ruff check $(DIFF_PYTHONS); \
		echo "> pyright"; pyright $(DIFF_PYTHONS); \
	fi

test:
	bats --timing ./tests/api_db_test.bats $(filter-out $@,$(MAKECMDGOALS));

up:
	uvicorn main:app \
		--port $(PORT) \
		--app-dir ./src \
		--reload

db:
	docker compose down --remove-orphans -v
	docker compose up dockerize
