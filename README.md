# Python Petstore API Tests

This project contains pytest API tests for the Swagger Petstore API.

## Setup

Python 3.13 or newer is recommended.

```powers
python -m pip install -r requirements.txt
python -m pytest --collect-only
```

If `python` resolves to the wrong interpreter on Windows, use `python3`:

```powers
python3 -m pip install pytest requests
python3 -m pytest --collect-only
```

## Running the Tests

Run the complete suite:

```powers
python -m pytest
```

Run one test:

```powers
python -m pytest test_swagger.py::test_update_pet_name
```

Run tests with verbose names and assertion details:

```powers
python -m pytest -v
```

## Project Structure

- `test_swagger.py` - API test cases
- `conftest.py` - pytest fixtures
- `clients/pet_client.py` - reusable Petstore API methods

`PetClient` provides methods for:

- Creating pets
- Getting pets by ID or status
- Updating pets
- Deleting pets

## Test Data and Cleanup

Tests create their own pet data where possible. The `created_pet` fixture creates a pet before a test and attempts to delete it during fixture teardown.

The fixture teardown removes the pet if it still exists. This prevents tests that already deleted their pet from failing cleanup.

## Known API Findings

The following behavior is observed from the live Swagger Petstore demo, but differs from the test expectations:

### Missing pet name

`POST /pet` accepts a Pet payload without a `name` field and returns `200`.

Expected validation behavior:

- Return a `400` client error.
- Not create a pet missing the required name.

The missing-name test currently records this as an API defect.
It is marked with pytest `xfail` so the suite remains usable while the API behavior is documented.

### Invalid pet ID format

Sending `"wrong_input"` as the Pet `id` to `POST /pet` returns `500` instead of a `400` or `405` client error.

The invalid-ID test currently records this as an API defect.
It is marked with pytest `xfail` so the suite remains usable while the API behavior is documented.

These findings demonstrate that the demo API does not consistently validate request fields or convert invalid input into appropriate client-error responses.

## Interview and Practice Checklist

Use this checklist as a review before continuing or presenting the project:

### Environment

- [ ] Confirm which Python interpreter runs tests in VS Code.
- [ ] Use the same interpreter for installing `pytest` and `requests`.
- [ ] Install dependencies with `python -m pip install -r requirements.txt`.
- [ ] Run tests with `python -m pytest -q`.
- [ ] Configure VS Code with **Python: Configure Tests** and pytest.
- [ ] Remember that `python` and `python3` can point to different environments on Windows.

### Test Structure

- [ ] Keep test setup in fixtures.
- [ ] Give each test its own pet data where possible.
- [ ] Do not depend on another test running first.
- [ ] Use descriptive test names.
- [ ] Keep reusable HTTP endpoint logic in `PetClient`.
- [ ] Put assertions in tests rather than hiding behavior in the client.
- [ ] Include status-code assertions and response-body assertions.
- [ ] Add custom pytest assertion messages for expected and actual values.
- [ ] Use negative assertions only when they describe meaningful behavior.

### HTTP and JSON

- [ ] Use `json=body` when sending a JSON dictionary.
- [ ] Remember that a Python dictionary is converted to a JSON request body.
- [ ] Access dictionary values with keys such as `pet["name"]`.
- [ ] Use the documented HTTP method: `PUT /pet` for updating a pet.
- [ ] Place the pet ID inside the PUT body rather than using `/pet/{petId}`.
- [ ] Send form data with `data=` only when the endpoint expects form fields.
- [ ] Include a timeout for each HTTP call.

### Fixture and Cleanup Practice

- [ ] Create a pet in setup and delete it in teardown.
- [ ] Use `yield` in a fixture when setup and teardown both are needed.
- [ ] Yield the value the test needs, such as the pet ID.
- [ ] Use `try/finally` for directly created test data.
- [ ] Treat `404` as successful cleanup when a test deleted the pet first.
- [ ] Do not let cleanup failures hide or replace the original test failure.
- [ ] Use unique IDs instead of fixed or low-range test IDs.
- [ ] Verify persistence with a GET after POST or PUT.

### Common Mistakes to Remember

- [ ] Missing comma after a function argument causes `"(" was not closed`.
- [ ] Remove extra `:` characters after `requests.get(...)` or `requests.post(...)`.
- [ ] Use `"id"` for the Petstore JSON field, not `"pet_id"`.
- [ ] Do not mutate a request dictionary unnecessarily; copy it when needed.
- [ ] Do not call `update_pet(pet_id, body)` if the endpoint only accepts a body.
- [ ] Do not use an integer larger than Java's `Long` range in IDs.
- [ ] Do not use `response.json()` when a server returns an empty response body.
- [ ] Do not expect a 400 or 405 when the live API returns 404 or 500.
- [ ] Remember that `raise_for_status()` raises on 4xx and 5xx responses.
- [ ] Remember that it does not verify a 2xx status with a required business result.

### Reporting API Defects

- [ ] Run a negative test before assuming it is a test bug.
- [ ] Record the exact request, status code, and response body.
- [ ] Mark reproducible API defects with pytest `xfail`.
- [ ] Explain that the API accepts a missing name instead of enforcing a 400.
- [ ] Explain that invalid string IDs can produce 500 instead of 400 or 405.
- [ ] Keep defect tests visible rather than deleting or silently skipping them.
