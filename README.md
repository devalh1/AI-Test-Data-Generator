
# AI-Assisted Test Data Generator

A Python-based tool that automatically generates test data from API specifications.

## Problem Statement

Creating valid, invalid, and boundary test data manually is time-consuming. This project aims to automate that process using API schemas.

## Proposed Solution

The application will allow testers to upload an OpenAPI specification, select an endpoint, and automatically generate test datasets.

## MVP Features

- OpenAPI specification upload (YAML/JSON)
- API endpoint selection
- Schema and constraint extraction
- Positive test data generation
- Negative test data generation
- Boundary-value generation
- Generated data validation
- JSON, CSV, and Excel export

## Technology Stack

- Python
- Streamlit
- OpenAPI
- PyYAML
- Faker
- JSON Schema
- Pydantic
- SQLite
- Git and GitHub

## Project Structure

- `parser/` - API specification parsing
- `generator/` - Test data generation
- `rules/` - Business rule evaluation
- `validator/` - Data validation
- `ai/` - Future AI integration
- `export/` - Dataset export
- `tests/` - Automated tests

## Current Status

The project currently has a working prototype with the following functionality:

- Parses OpenAPI specifications written in YAML.
- Extracts API endpoints, HTTP methods, and request-body schemas.
- Generates positive and negative test data.
- Generates boundary-value test cases for string and integer constraints.
- Tests email formats and missing required fields.
- Exports generated test cases to JSON.
- Executes generated test cases against a local FastAPI mock API.
- Evaluates API responses and generates a JSON execution report.

**Current test results:**
- Total test cases: 15
- Passed: 15
- Failed: 0
- Errors: 0

The prototype has also been tested on both macOS and Windows.

AI-assisted generation and the web interface are planned for future development.

## Future Enhancements

- AI-assisted scenario suggestions
- Business rule interpretation
- Pairwise testing
- Historical dataset management
- API test execution
