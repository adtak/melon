.PHONY: format black isort test

format: black isort

black:
				poetry run black .

isort:
				poetry run isort .

mypy:
				poetry run mypy .

test:
				poetry run pytest
