.PHONY: format
format: black ruff

.PHONY: black
black:
				poetry run black melon_iac/*

.PHONY: ruff
ruff:
				poetry run ruff check melon_iac/* --no-cache --fix

.PHONY: mypy
mypy:
				poetry run mypy .
