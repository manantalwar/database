run:
	LRC_DATABASE_SECRET_KEY=abc123 LRC_DATABASE_DEBUG=1 ./lrc_database/manage.py runserver 0.0.0.0:8000

win_run:
	set LRC_DATABASE_SECRET_KEY=abc123
	set LRC_DATABASE_DEBUG=1
	python lrc_database\manage.py runserver

run_docker:
	LRC_DATABASE_SECRET_KEY=abc123 docker compose up

check_bandit:
	bandit lrc_database --recursive --configfile pyproject.toml

check_black:
	black lrc_database --check

check_isort:
	isort lrc_database --check --diff

check_mypy:
	cd ./lrc_database && mypy . --config ../pyproject.toml --show-traceback

check_code: check_bandit check_mypy

check_formatting: check_black check_isort

check: check_code check_formatting

# isort must come before black because it might change the order of imports,
# while black never will.
format_black: format_isort
	black lrc_database

format_isort:
	isort lrc_database

format: format_black format_isort

reset_database:
	rm -rf ./lrc_database/main/migrations/*.py
	touch ./lrc_database/main/migrations/__init__.py
	rm -f ./lrc_database/db.sqlite3
	./lrc_database/manage.py makemigrations main
	./lrc_database/manage.py migrate
	./lrc_database/manage.py bootstrapdatabase

win_reset:
	del lrc_database\main\migrations\*.py
	type nul > lrc_database\main\migrations\__init__.py
	del lrc_database\db.sqlite3
	python lrc_database\manage.py makemigrations main
	python lrc_database\manage.py migrate
	python lrc_database\manage.py bootstrapdatabase

migrate:
	./lrc_database/manage.py makemigrations main
	./lrc_database/manage.py migrate

win_migrate:
	python lrc_database\manage.py makemigrations main
	python lrc_database\manage.py migrate

install_git_hooks:
	cp .git-hooks/* .git/hooks

install_systemd_service:
	cp lrc-database.service /etc/systemd/system/lrc-database.service
	systemctl daemon-reload

restart:
	systemctl restart lrc-database.service

logs:
	journalctl -u lrc-database.service

.PHONY: *
