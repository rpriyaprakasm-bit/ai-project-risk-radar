# Architecture

## High-level flow

1. **Collector** gathers project data from one or more tools and writes a normalized JSON file.
2. **Analyzer** sends that data + a carefully designed prompt to Claude and receives a structured Risk Report.
3. **Reporter** publishes the report (GitHub Issue today, can be extended to Slack, email, etc.).

## Why this design?

- **Separation of concerns** — each layer has one job.
- **Extensibility** — new tools only require a new collector.
- **Testability** — you can run the analyzer on saved JSON without live APIs.
- **Portfolio clarity** — reviewers can immediately see clean architecture.
