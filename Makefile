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
		set -e; \
		echo "> ruff (fix imports & quotes)"; uv run ruff check --select F401,Q,I --fix --quiet $(DIFF_PYTHONS); \
		echo "> black (code formatting)"; uv run black --config $(SETTINGS_PATH) -q $(DIFF_PYTHONS); \
	fi

lint:
	@if [[ ! -z "$(DIFF_PYTHONS)" ]]; then \
		set -e; \
		echo "> pylint (code analysis)"; uv run pylint --rcfile=$(SETTINGS_PATH) -sn $(DIFF_PYTHONS); \
		echo "> ruff (style & error checking)"; uv run ruff check --quiet $(DIFF_PYTHONS); \
		echo "> pyright (type checking)"; uv run pyright $(DIFF_PYTHONS) | grep -v "0 errors, 0 warnings" || true; \
	fi
	@if command -v cspell > /dev/null; then \
		echo "> cspell (spell checking)"; cspell --gitignore --no-progress --no-summary --no-must-find-files $(DIFF_FILES); \
	fi;

test:
	@uv run coverage erase
	@bats --timing ./tests/api_db_test.bats
	@uv run coverage report --show-missing --skip-covered --fail-under 90
	@uv run coverage html

up:
	uv run uvicorn main:app \
		--port $(PORT) \
		--app-dir ./src \
		--reload

db:
	docker compose down --remove-orphans -v
	docker compose up dockerize
