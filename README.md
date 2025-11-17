# DevOps Activity – Flask API with GitHub Actions

This repo contains a tiny Flask API plus CI/CD-style automation with GitHub Actions,
based on the DevOps Activity instructions (Advanced GitHub Actions for a Flask Application).

## Flask application

**Main file:** `app.py`

Endpoints implemented:

- `GET /hello`  
  Returns a simple JSON payload:

  ```json
  { "message": "Hello, World!" }
  ```

- `POST /echo`  
  Accepts a JSON body and echoes it back with HTTP `201 Created`.  
  Example request/response body:

  ```json
  { "msg": "ping" }
  ```

- `PUT /items/<item_id>`  
  Creates or updates a tiny in-memory item identified by `item_id`. The request body
  should be JSON (e.g. `{ "name": "example", "value": 42 }`).  
  The response looks like:

  ```json
  {
    "id": 1,
    "data": { "name": "example", "value": 42 }
  }
  ```

- `DELETE /items/<item_id>`  
  Deletes the item with the given `item_id` from the in-memory store.

  - If the item exists, returns HTTP 200 and the deleted payload.
  - If the item does not exist, returns HTTP 404 with a small error JSON.

> Note: the in-memory store is only for demo/testing. It resets every time the
> process restarts and is **not** suitable for production use.

## Tests

Tests live in `test_app.py` and use `pytest` + `pytest-cov`:

- `test_hello()` – verifies `/hello` returns status 200 and the expected JSON.
- `test_echo()` – verifies `/echo` returns status 201 and echoes the JSON payload.
- `test_update_item_creates_or_updates()` – ensures `PUT /items/<id>` sets and
  then updates the same id.
- `test_delete_item_existing()` – ensures `DELETE /items/<id>` works when the item exists.
- `test_delete_item_missing()` – ensures a missing item returns 404 with an error field.

Run locally with:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pytest -q
```

## GitHub Actions workflows

Located under `.github/workflows/`:

1. **`test.yml` – Python Application Test**  
   - Triggers on `push` and `pull_request`.
   - Runs on Ubuntu with a matrix of Python `3.10`, `3.11`, and `3.12`.
   - Installs dependencies from `requirements.txt`.
   - Runs `pytest` with coverage and generates `coverage.xml`.
   - Uploads coverage to Codecov via `codecov/codecov-action@v2`
     (requires `CODECOV_TOKEN` for private repos).

2. **`lint.yml` – Python Linting**  
   - Triggers on `push` and `pull_request`.
   - Installs `flake8` and runs it on `app.py` and `test_app.py`.

3. **`codeql-analysis.yml` – CodeQL Security Scan**  
   - Triggers on pushes and pull requests targeting `main`.
   - Uses GitHub's CodeQL actions to scan the Python code for common security issues.

## Dependabot

`.github/dependabot.yml` is configured to:

- Watch the `pip` ecosystem in the repository root (`/`).
- Create weekly PRs for outdated Python dependencies.