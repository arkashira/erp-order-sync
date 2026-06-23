# STORIES.md

## Project: erp-order-sync
**Goal:** Provide a reliable, extensible Python library that detects ERP connection failures, logs detailed diagnostics, and notifies stakeholders through configurable channels. The MVP must be production‑ready, fully tested, and easy to integrate into existing ERP integration pipelines.

---

## Epics & Backlog

| Epic | Description |
|------|-------------|
| **E1 – Core Error Handling** | Detect and classify ERP connection errors, capture context, and surface a uniform exception hierarchy. |
| **E2 – Notification Engine** | Deliver real‑time alerts via configurable channels (email, Slack, webhook) with templated messages. |
| **E3 – Logging & Auditing** | Persist structured logs to file/JSON and optionally to external log aggregators (e.g., ELK, Splunk). |
| **E4 – Configuration & Extensibility** | Provide a declarative YAML/JSON config and plugin hooks for custom notifiers or log sinks. |
| **E5 – Testability & CI** | Achieve >90 % unit‑test coverage, include integration test harness, and embed CI pipelines. |
| **E6 – Documentation & SDK** | Auto‑generate API docs, usage examples, and a thin wrapper SDK for easy consumption. |

---

## MVP Stories (ordered for incremental delivery)

### Epic E1 – Core Error Handling
| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| **E1‑01** | **As a developer**, I want `ERPOrderSync.handle_connection_error(exc)` to accept any exception and classify it as *Transient* or *Fatal*, so that downstream logic can decide whether to retry. | - Function returns a `ConnectionErrorInfo` object with fields: `type` (Transient/Fatal), `original_exception`, `timestamp`. <br>- Classification rules are documented and unit‑tested (e.g., `TimeoutError` → Transient, `AuthenticationError` → Fatal). |
| **E1‑02** | **As a developer**, I want the library to automatically retry transient errors up to a configurable limit, so that temporary glitches are hidden from the caller. | - Retries use exponential back‑off (base = 2, jitter ≤ 100 ms). <br>- Configurable `max_retries` (default = 3). <br>- After exhausting retries, the same `ConnectionErrorInfo` is returned with `type=Fatal`. |
| **E1‑03** | **As a support engineer**, I need the error handler to capture the full stack trace and ERP request payload, so that troubleshooting is fast. | - `ConnectionErrorInfo` includes `stack_trace` (string) and optional `request_context` dict. <br>- Payload is redacted according to a configurable `sensitive_fields` list. |

### Epic E2 – Notification Engine
| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| **E2‑01** | **As an operations manager**, I want the system to send an email alert when a fatal error occurs, so that I can act immediately. | - Email provider configurable via SMTP settings or SendGrid API key. <br>- Subject line includes ERP name and error type. <br>- Body uses a Jinja2 template populated with `ConnectionErrorInfo`. |
| **E2‑02** | **As a DevOps engineer**, I want Slack notifications for all connection errors, so that the incident channel stays informed. | - Slack webhook URL configurable. <br>- Message includes emoji based on severity (⚠️ for transient, ❌ for fatal). |
| **E2‑03** | **As a system integrator**, I want to register a custom webhook URL to receive JSON payloads for every error, so that my monitoring platform can ingest them. | - Payload matches the `ConnectionErrorInfo` schema. <br>- HTTP POST with retry on 5xx responses (max 2 retries). |
| **E2‑04** | **As a product owner**, I want to enable/disable each notification channel per environment (dev, staging, prod), so that we don’t spam during testing. | - Config file supports per‑environment toggles. <br>- Unit tests verify that disabled channels produce no outbound calls. |

### Epic E3 – Logging & Auditing
| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| **E3‑01** | **As a security auditor**, I need all error events written to a structured JSON log file, so that they can be ingested by SIEM tools. | - Log file path configurable. <br>- Each line is a valid JSON object with fields: timestamp, erp_id, error_type, severity, request_id, etc. |
| **E3‑02** | **As a site reliability engineer**, I want optional integration with the `loguru` logger, so that existing logging pipelines remain untouched. | - If `loguru` is present, library uses `loguru.logger`; otherwise falls back to standard `logging`. |
| **E3‑03** | **As a developer**, I want to tag each log entry with a correlation ID that can be passed from upstream code, so that traces are end‑to‑end. | - `handle_connection_error` accepts optional `correlation_id` argument; it propagates to `ConnectionErrorInfo` and all logs/notifications. |

### Epic E4 – Configuration & Extensibility
| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| **E4‑01** | **As a DevOps engineer**, I want to configure the library via a single `erp_sync.yaml` file, so that deployment is declarative. | - YAML schema validated on load (using `pydantic` or `cerberus`). <br>- Supports sections: `retry`, `notifications`, `logging`, `sensitive_fields`. |
| **E4‑02** | **As a plugin developer**, I want to add a new notifier by implementing a `BaseNotifier` subclass, so that the core library stays unchanged. | - `BaseNotifier` defines `notify(error_info: ConnectionErrorInfo) -> None`. <br>- Registration via entry‑point `erp_order_sync.notifiers`. <br>- Unit test that a dummy notifier receives calls. |
| **E4‑03** | **As a security lead**, I need the ability to mask/redact fields in the request payload before they are logged or sent, so that PII is never exposed. | - Configurable `sensitive_fields` list (e.g., `["password","ssn"]`). <br>- Redaction replaces values with `"***REDACTED***"` in all outputs. |

### Epic E5 – Testability & CI
| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| **E5‑01** | **As a QA engineer**, I want a full test suite that can be run with `pytest -q`, so that CI can verify correctness on every commit. | - Tests cover all error classifications, retry logic, each notifier (mocked), and config validation. <br>- Coverage report ≥ 90 % (excluding generated docs). |
| **E5‑02** | **As a release manager**, I want GitHub Actions workflow that lints, runs tests, and builds a wheel, so that releases are automated. | - Workflow file `.github/workflows/ci.yml` includes steps: `ruff` lint, `pytest`, `coverage`, `build`. |
| **E5‑03** | **As a developer**, I want integration tests that spin up a mock SMTP server and Slack webhook, so that external dependencies are exercised. | - Uses `aiosmtpd` and `httpx` mock server fixtures. <br>- Tests run in CI without external credentials. |

### Epic E6 – Documentation & SDK
| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| **E6‑01** | **As a new user**, I need a quick‑start guide in the README with a minimal code snippet, so I can try the library in <5 minutes. | - README contains a “Getting Started” section with pip install, config file example, and a 5‑line Python demo. |
| **E6‑02** | **As a developer**, I want API reference generated by `mkdocstrings`, so that I can explore class methods without leaving my IDE. | - `docs/` folder contains `mkdocs.yml` and generated HTML on GitHub Pages. |
| **E6‑03** | **As a partner**, I need a thin wrapper SDK (`erp_sync_sdk`) that abstracts config loading and provides a single `sync()` call, so integration is trivial. | - SDK package publishes on PyPI, imports `ERPOrderSync` internally, and exposes `sync()` that returns success/failure boolean. |

---

## Release Milestones

| Milestone | Included Epics | Target Date |
|-----------|----------------|-------------|
| **M1 – Core & Logging** | E1, E3 | 2 weeks |
| **M2 – Email & Slack Notifiers** | E2 (E2‑01, E2‑02) | +1 week |
| **M3 – Config & Extensibility** | E4, E2‑03, E2‑04 | +1 week |
| **M4 – Full Test Suite & CI** | E5, E2‑03 (mock), E4‑02 | +1 week |
| **M5 – Docs, SDK & Release** | E6, packaging | +1 week |

---

*All stories are written to be independently testable and shippable. Prioritization follows the “error detection → alert → audit → configure → automate → document” flow, ensuring a functional MVP after Milestone M1.*
