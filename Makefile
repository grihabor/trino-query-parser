PACKAGE_DIR  := src/trino_query_parser
GRAMMAR_URL  := https://raw.githubusercontent.com/trinodb/trino/405/core/trino-parser/src/main/antlr4/io/trino/sql/parser/SqlBase.g4
GRAMMAR_G4   := $(PACKAGE_DIR)/SqlBase.g4

$(GRAMMAR_G4):
	curl -s -o "$(GRAMMAR_G4)" "$(GRAMMAR_URL)"


.PHONY: generate-code
generate-code: $(GRAMMAR_G4)
	antlr4 -Dlanguage=Python3 -visitor "$(GRAMMAR_G4)"


.PHONY: format
format:
	black src/ tests/


.PHONY: test
test: test-readme test-unit

.PHONY: test-readme
test-readme:
	python -m doctest -v README.rst

.PHONY: test-unit
test-unit:
	pytest tests/
