
# Test Data Design Document
## AI-Assisted Test Data Generator

### 1. Project Objective
To develop a web-based application that automatically generates realistic test data from API specifications, reducing manual test-data preparation effort.

### 2. Target Users
- QA Engineers
- Software Testers
- Backend Developers
- Startups and Enterprise Development Teams

### 3. Problem Statement
Manually creating positive, negative and boundary test data is time-consuming. Maintaining test data as API requirements change also requires additional effort.

### 4. Proposed Solution
The application will accept an OpenAPI specification, extract endpoint and schema information, and generate test datasets automatically.

### 5. Input
- OpenAPI specification in YAML or JSON format.
- Selected API endpoint.
- Test-data categories.
- Desired number of records or custom category counts.

### 6. Processing
1. Parse the OpenAPI specification.
2. Extract available endpoints.
3. Allow endpoint selection.
4. Extract request schema and constraints.
5. Generate positive, negative and boundary data.
6. Validate generated records.
7. Label expected validation outcomes.

### 7. Output
- JSON datasets
- CSV datasets
- Excel datasets
- Validation summaries
- Test coverage information

### 8. MVP Features
- OpenAPI upload and parsing
- Endpoint selection
- Schema extraction
- Positive data generation
- Negative data generation
- Boundary-value generation
- Schema validation
- Dataset export

### 9. Technology Stack
- Python
- Streamlit
- PyYAML
- OpenAPI specification validator
- Faker
- JSON Schema
- Pydantic
- SQLite
- Git and GitHub

### 10. Future Enhancements
- AI-assisted scenario suggestions
- Business-rule interpretation
- Pairwise testing
- Historical dataset management
- API test execution

### 11. MVP Limitations
- No chatbot interface.
- No AI integration in the first version.
- No simultaneous multi-endpoint generation.
- No automated API execution.
