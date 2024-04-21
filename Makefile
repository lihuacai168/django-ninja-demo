# Makefile

# Defining the directory variables
PROJECT_DIR = .
COVERAGE_DIR = htmlcov

# Run Django tests and collect coverage data
test:
	@echo "Running tests with coverage..."
	@coverage run --source='$(PROJECT_DIR)' manage.py test

# Generate an HTML coverage report
html-report:
	@echo "Generating HTML coverage report..."
	@coverage html

# Open the HTML coverage report in the browser
open-report:
	@echo "Opening HTML coverage report..."
	@open $(COVERAGE_DIR)/index.html

# Combine commands: run tests, generate and open HTML coverage report
coverage: test html-report open-report

# Marking targets as phony, they are not files
.PHONY: test html-report open-report coverage