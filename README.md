
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

Initial development environment and project structure established.

Core functionality is under development.

## Future Enhancements

- AI-assisted scenario suggestions
- Business rule interpretation
- Pairwise testing
- Historical dataset management
- API test execution
