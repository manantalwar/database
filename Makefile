format:
	isort lrc_database
	black lrc_database --line-length 120

check:
	flake8 lrc_database
	cd ./lrc_database && mypy . --config ../setup.cfg

reset_database:
	rm -rf ./lrc_database/main/migrations/*.py
	touch ./lrc_database/main/migrations/__init__.py
	rm -f ./lrc_database/db.sqlite3
	./lrc_database/manage.py makemigrations main
	./lrc_database/manage.py migrate
	./lrc_database/manage.py bootstrapdatabase --user-count=10
