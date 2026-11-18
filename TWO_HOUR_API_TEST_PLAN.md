# Two-Hour API Test Practice Plan

Use this plan for an interview-style API testing exercise with an unfamiliar or randomly selected API.

## Recommended Scope

Aim for approximately 12-15 focused tests.

| Area | Recommended count | Coverage |
|---|---:|---|
| Create | 3 | Success, missing required field, invalid payload |
| Read | 3 | Valid ID, missing ID, list or filter |
| Update | 2 | Success, missing entity |
| Delete | 2 | Success with follow-up GET, missing entity |
| Authentication or errors | 2 | Unauthorized request, invalid endpoint or malformed request |
| Smoke test | 1 | Health, version, or base endpoint |

For CRUD APIs, prioritize POST, GET, PUT or PATCH, and DELETE.

Each test should validate more than status code when practical:

- Response status
- Response JSON structure
- Required keys
- Created ID
- Updated fields
- Deleted entity no longer exists
- Error response format
- Unintended changes

## 0:00-0:15 - Inspect the API

- [ ] Find Swagger/OpenAPI documentation or API documentation.
- [ ] Identify the base URL.
- [ ] Identify authentication requirements.
- [ ] Identify required headers.
- [ ] Find the resource to use for CRUD tests.
- [ ] Identify required and optional fields.
- [ ] Identify documented status codes.
- [ ] Confirm whether the API is live or local.
- [ ] Send one manual request to confirm setup.

## 0:15-0:30 - Set Up the Project

Create a small project structure:

```text
tests/
clients/
conftest.py
README.md
requirements.txt
.gitignore
```

Install dependencies:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install pytest requests
python -m pip freeze > requirements.txt
```

Configure VS Code pytest discovery if needed.

## 0:30-0:45 - Build a Small API Client

Implement only the operations needed for the exercise:

- `create_resource()`
- `get_resource()`
- `update_resource()`
- `delete_resource()`

Keep these concerns in the client:

- Base URL
- Authentication
- Shared session
- Timeout
- JSON or form-data encoding

Keep assertions in the tests.

## 0:45-1:10 - Create Core CRUD Tests

Write approximately seven tests:

1. Create a resource successfully.
2. Get the created resource.
3. Update a field.
4. Verify the updated field persists.
5. Delete the resource.
6. Verify deletion with another GET.
7. Test a status, filter, or list endpoint.

Use a fixture to create a resource before fixture-based tests and delete it during teardown.

Use unique IDs or unique names where supported.

## 1:10-1:30 - Add Negative Tests

Write approximately four tests:

1. Missing required field.
2. Invalid payload type or value.
3. Resource not found.
4. Unauthorized or invalid authentication request.

If a negative test exposes a reproducible API defect:

- Record the request.
- Record the actual status code.
- Record the actual response body.
- Compare it with the documented behavior.
- Decide whether to mark it `xfail` or report it as a defect.

Do not silently change normal test expectations to match incorrect API behavior.

## 1:30-1:45 - Improve Assertions and Cleanup

Include:

- Custom expected-versus-actual messages.
- Response body details for unexpected HTTP failures.
- Required JSON keys.
- Collection element types.
- Preservation of unrelated fields.
- Cleanup verification.

Use a `try/finally` block or pytest fixture for data cleanup.

Avoid a broad status assertion such as:

```python
assert response.status_code in (200, 201, 204)
```

Use the exact documented status for the operation unless the API contract clearly allows alternatives.

## 1:45-2:00 - Run and Document

- [ ] Run the complete suite.
- [ ] Fix test failures and environment problems.
- [ ] Verify passing and xfailed test counts.
- [ ] Document setup and run commands.
- [ ] Document test coverage.
- [ ] Document known API defects with exact observations.
- [ ] Prepare to explain the hardest defect found.

## Practical Limitations

Do not spend most of the two hours on:

- CI configuration
- Heavy parameterization
- Excessive abstractions
- A custom framework
- Tests for every endpoint
- Complex reporting libraries
- Mocking the API before testing the real API

## Interview Demonstration Goal

By the end of two hours, demonstrate that you can:

1. Understand Swagger or OpenAPI documentation.
2. Create a reusable HTTP client.
3. Use pytest fixtures for isolated setup and cleanup.
4. Validate persistence rather than only status codes.
5. Diagnose and document API defects.
6. Produce a reproducible test suite.

A good practical result is approximately 10-12 passing tests with one or two documented expected failures, rather than 30 shallow status-code checks.
