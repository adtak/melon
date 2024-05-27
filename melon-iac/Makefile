.PHONY: format
format: black ruff

.PHONY: black
black:
				poetry run black .

.PHONY: ruff
ruff:
				poetry run ruff check melon_iac/* lambda/* tests/* --no-cache --fix

.PHONY: mypy
mypy:
				poetry run mypy .
