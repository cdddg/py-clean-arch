SETTINGS_PATH ?= ./pyproject.toml
PORT ?= 8000
GIT_ARGS := --name-only --diff-filter=d --cached
ifneq ($(DIFF_SRC),)
	GIT_ARGS := --name-only --diff-filter=d $(DIFF_SRC)...HEAD
endif
DIFF_FILES = `git diff $(GIT_ARGS) | grep .py$$ | grep -v migrations`


format:
	echo $(DIFF_FILES) | sed -e 's/ /\n/g' ;
	@if [[ ! -z ${DIFF_FILES} ]]; then \
		remove-print-statements $(DIFF_FILES); \
		autoflake --remove-all-unused-imports --ignore-init-module-imports -r -i $(DIFF_FILES); \
		isort -settings_path=$(SETTINGS_PATH) --quiet $(DIFF_FILES); \
		black --config $(SETTINGS_PATH) $(DIFF_FILES); \
	fi

lint:
	echo $(DIFF_FILES) | sed -e 's/ /\n/g' ;
	@if [[ ! -z $(DIFF_FILES) ]]; then \
		echo pylint... ; \
		pylint --rcfile=$(SETTINGS_PATH) --load-plugins=pylint_quotes -sn -v $(DIFF_FILES); \
	fi


test:
	TEST=true pytest --cache-clear --log-level=ERROR -W=error -sxvv $(filter-out $@,$(MAKECMDGOALS));


up:
	uvicorn main:app \
		--port $(PORT) \
		--app-dir ./src \
		--reload
