.PHONY: format
format: black ruff

.PHONY: black
black:
				poetry run black *.py

.PHONY: ruff
ruff:
				poetry run ruff check *.py --no-cache --fix

.PHONY: mypy
mypy:
				poetry run mypy .
