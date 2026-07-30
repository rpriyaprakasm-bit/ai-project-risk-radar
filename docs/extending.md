# Extending the Risk Radar to Other Tools

The system is designed so you can add new data sources without touching the analyzer or reporter.

## Required Interface

Every collector must return a dictionary with this shape:

```json
{
  "source": "jira" | "linear" | "notion" | ...,
  "collected_at": "2026-07-30T12:00:00Z",
  "issues": [
    {
      "id": "PROJ-123",
      "title": "Fix login timeout",
      "state": "In Progress",
      "labels": ["bug", "frontend"],
      "assignees": ["alice"],
      "created_at": "...",
      "updated_at": "...",
      "due_date": "2026-08-01",
      "body": "Description text...",
      "comments_count": 4,
      "url": "https://..."
    }
  ],
  "pull_requests": [],          // optional
  "metadata": {}                // optional
}
```

## Steps to Add a New Collector

1. Create `src/collectors/your_tool_collector.py`
2. Implement a `collect()` function (or class) that returns the format above
3. Save the result to `data/project_data.json`
4. Update the GitHub Action workflow to call your new collector
5. (Optional) Add any required API keys as GitHub Secrets

Because the Risk Analyzer only reads `data/project_data.json`, it will work with any source that follows the contract.
