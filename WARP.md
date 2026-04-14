# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

Project: Descargador de Tareas JIRA (Python CLI)

Commands

- Setup (recommended virtualenv on macOS/Linux)
  - python3 -m venv .venv
  - source .venv/bin/activate
  - pip3 install -r requirements.txt

- Run the CLI
  - python3 main.py

- Linting/Formatting
  - No linters or formatters are configured in this repo.

- Tests
  - There are no tests included in this repo.

Important runtime notes

- Python: 3.7+
- Dependencies: requests (declared in requirements.txt)
- Network: interacts with Atlassian JIRA REST API v3 endpoints.
- Side effects (outputs):
  - CSV: {PROJECT_KEY}_issues_{YYYYMMDD_HHMMSS}.csv in repo root
  - Attachments (optional): {PROJECT_KEY}_attachments_{YYYYMMDD_HHMMSS}/<ISSUE-KEY>/prefixed files

High-level architecture and flow

- Entry point: main.py
  - Provides an interactive console flow asking for: JIRA base URL, user email, API token, and project key.
  - Instantiates JiraDownloader and orchestrates the end-to-end process: connect → fetch issues → transform → export CSV → optional attachment download.

- Core class: JiraDownloader (in main.py)
  - HTTP/session setup
    - Uses requests.Session with basic auth (username + API token) and JSON headers against {base_url}/rest/api/3/*.
  - Connectivity check (test_connection)
    - GET /myself to validate credentials and prints connected user name.
  - Issue retrieval (get_all_issues)
    - Paginates with startAt/maxResults (100/page), builds JQL for project ordering by key.
    - Requests a focused field set to reduce payload, expands changelog for history.
    - Rate-limits with a short sleep between page fetches; prints progress and total.
  - Data extraction (extract_issue_data)
    - Normalizes core fields (summary, status, type, priority, assignee, reporter, timestamps, labels, components, fixVersions).
    - Flattens comments into a single string with author and timestamp.
    - Flattens changelog histories into a single string describing field transitions.
    - Cleans and truncates long text fields to 1000 chars; supports Atlassian Document Format (ADF) via extract_text_from_adf.
  - CSV export (export_to_csv)
    - Emits a UTF-8 CSV with header inferred from the first row’s keys; prints destination.
  - Attachments
    - get_attachments extracts file metadata from each issue.
    - download_attachment streams file content; ensures directory creation; handles errors gracefully.
    - download_all_attachments iterates issues, sanitizes filenames, prefixes with issue key, skips existing files, rate-limits, and prints per-file progress.

- CLI orchestration (main)
  - Builds a timestamp once per run to keep CSV and attachments consistently grouped.
  - Shows progress during processing every N issues (50 by default in this implementation).

Configuration

- config_example.py is a sample showing how configuration could be externalized (JIRA credentials, export and performance options). It is not imported by main.py; treat it as reference only unless you add an import path and usage.

Repository layout notes

- Top-level Python sources: main.py, config_example.py, requirements.txt, README.md.
- There is a nested directory “EJEMPLO EXTRACCIÓN CON FICHEROS/…” containing sample artifacts (including a pytest.ini under a testing folder for unrelated example content). These are not part of the runnable CLI and can be ignored for development here.
