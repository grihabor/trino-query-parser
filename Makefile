all: help 

.PHONY: help
help: ## Show help
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

TRINO_VERSION   ?= 421
PACKAGE_DIR     := src/trino_query_parser

GRAMMAR_URL      = https://raw.githubusercontent.com/trinodb/trino/$(TRINO_VERSION)/core/trino-parser/src/main/antlr4/io/trino/sql/parser/SqlBase.g4
GRAMMAR_G4      := $(PACKAGE_DIR)/SqlBase.g4

CURL            := curl -s -L --fail-with-body

$(GRAMMAR_G4):
	$(CURL) -o "$(GRAMMAR_G4)" "$(GRAMMAR_URL)" || (rm "$(GRAMMAR_G4)" && exit 1)

ANTLR4_VERSION  := $(shell grep -o -E 'antlr4-python3-runtime==[0-9]+.[0-9]+.[0-9]+' pyproject.toml | awk -F= '{print $$3}')
ANTRL4_JAR      := antlr-$(ANTLR4_VERSION)-complete.jar
ANTLR4_URL      := https://www.antlr.org/download/$(ANTRL4_JAR)
ANTLR4_JAR_PATH := build/$(ANTRL4_JAR)
ANTLR4          := java -cp "$(ANTLR4_JAR_PATH)" org.antlr.v4.Tool

.PHONY: antlr4-version
antlr4-version:
	@echo $(ANTLR4_VERSION)

build:
	mkdir -p build

$(ANTLR4_JAR_PATH): build
	$(CURL) -o "$(ANTLR4_JAR_PATH)" "$(ANTLR4_URL)"

.PHONY: generate-code
generate-code: $(ANTLR4_JAR_PATH) $(GRAMMAR_G4) ## Generate python parser code
	$(ANTLR4) -Dlanguage=Python3 -visitor "$(GRAMMAR_G4)"

.PHONY: format
format: format-isort format-black ## Format files

.PHONY: format-black
format-black:
	black src/ tests/

.PHONY: format-isort
format-isort:
	isort src/ tests/

.PHONY: test
test: test-readme test-unit ## Run tests

.PHONY: test-readme
test-readme:
	python -m doctest -v README.rst

.PHONY: test-unit
test-unit:
	pytest tests/
