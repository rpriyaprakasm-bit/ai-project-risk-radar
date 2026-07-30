"""
GitHub data collector.
Fetches open issues and recent pull requests for risk analysis.
Falls back to realistic demo data when the repo is empty.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

import urllib.request


def _github_api(url: str, token: str) -> Any:
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "AI-Project-Risk-Radar",
        },
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def collect() -> Dict[str, Any]:
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")  # e.g. owner/repo

    if not token or not repo:
        print("Warning: GITHUB_TOKEN or GITHUB_REPOSITORY not set. Using demo data.")
        return _demo_data()

    owner, name = repo.split("/")

    # Fetch open issues
    issues_url = f"https://api.github.com/repos/{owner}/{name}/issues?state=open&per_page=50"
    raw_issues = _github_api(issues_url, token)

    issues = []
    for item in raw_issues:
        if "pull_request" in item:
            continue  # skip PRs in issues endpoint
        issues.append({
            "id": item["number"],
            "title": item["title"],
            "state": item["state"],
            "labels": [l["name"] for l in item.get("labels", [])],
            "assignees": [a["login"] for a in item.get("assignees", [])],
            "created_at": item["created_at"],
            "updated_at": item["updated_at"],
            "due_date": None,
            "body": (item.get("body") or "")[:1500],
            "comments_count": item.get("comments", 0),
            "url": item["html_url"],
        })

    # Fetch recent open PRs
    prs_url = f"https://api.github.com/repos/{owner}/{name}/pulls?state=open&per_page=20"
    raw_prs = _github_api(prs_url, token)
    pull_requests = []
    for pr in raw_prs:
        pull_requests.append({
            "id": pr["number"],
            "title": pr["title"],
            "state": pr["state"],
            "user": pr["user"]["login"],
            "created_at": pr["created_at"],
            "updated_at": pr["updated_at"],
            "labels": [l["name"] for l in pr.get("labels", [])],
            "url": pr["html_url"],
        })

    # Empty repo → use demo data so portfolio still shows a full report
    if len(issues) == 0 and len(pull_requests) == 0:
        print("No open issues/PRs found. Using realistic demo data for the report.")
        return _demo_data()

    data = {
        "source": "github",
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "repository": repo,
        "issues": issues,
        "pull_requests": pull_requests,
        "metadata": {
            "open_issues_count": len(issues),
            "open_prs_count": len(pull_requests),
        },
    }

    out_path = Path("data/project_data.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(data, indent=2))
    print(f"Collected {len(issues)} issues and {len(pull_requests)} PRs → {out_path}")
    return data


def _demo_data() -> Dict[str, Any]:
    """Realistic demo data so the project works even on an empty repo."""
    data = {
        "source": "github-demo",
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "repository": "demo/project",
        "issues": [
            {
                "id": 42,
                "title": "Payment gateway integration is blocked by missing API keys",
                "state": "open",
                "labels": ["blocker", "backend", "high-priority"],
                "assignees": ["alice"],
                "created_at": "2026-07-10T09:00:00Z",
                "updated_at": "2026-07-28T14:00:00Z",
                "due_date": "2026-07-25",
                "body": "We cannot proceed with the checkout flow until the payment provider gives us production keys. Waiting for 2 weeks already.",
                "comments_count": 8,
                "url": "https://github.com/demo/project/issues/42",
            },
            {
                "id": 51,
                "title": "Add new discount engine for Black Friday",
                "state": "open",
                "labels": ["feature", "unestimated"],
                "assignees": [],
                "created_at": "2026-07-27T11:00:00Z",
                "updated_at": "2026-07-27T11:00:00Z",
                "due_date": None,
                "body": "Marketing wants a completely new discount rules engine. No estimate yet.",
                "comments_count": 1,
                "url": "https://github.com/demo/project/issues/51",
            },
            {
                "id": 38,
                "title": "Fix flaky tests in checkout suite",
                "state": "open",
                "labels": ["bug", "quality"],
                "assignees": ["bob"],
                "created_at": "2026-07-05T08:00:00Z",
                "updated_at": "2026-07-20T16:00:00Z",
                "due_date": "2026-07-15",
                "body": "Tests fail randomly on CI. Has been open for a while.",
                "comments_count": 12,
                "url": "https://github.com/demo/project/issues/38",
            },
            {
                "id": 55,
                "title": "Update user profile page",
                "state": "open",
                "labels": ["frontend"],
                "assignees": ["alice"],
                "created_at": "2026-07-22T10:00:00Z",
                "updated_at": "2026-07-29T09:00:00Z",
                "due_date": None,
                "body": "Small UI improvements.",
                "comments_count": 3,
                "url": "https://github.com/demo/project/issues/55",
            },
            {
                "id": 29,
                "title": "Critical: Database migration for new order schema",
                "state": "open",
                "labels": ["backend", "high-priority", "database"],
                "assignees": ["alice"],
                "created_at": "2026-07-01T12:00:00Z",
                "updated_at": "2026-07-25T18:00:00Z",
                "due_date": "2026-07-20",
                "body": "This is required before we can ship the new order flow. Alice is the only one who knows the old schema.",
                "comments_count": 15,
                "url": "https://github.com/demo/project/issues/29",
            },
        ],
        "pull_requests": [
            {
                "id": 88,
                "title": "WIP: Payment provider sandbox integration",
                "state": "open",
                "user": "alice",
                "created_at": "2026-07-18T10:00:00Z",
                "updated_at": "2026-07-28T11:00:00Z",
                "labels": ["wip"],
                "url": "https://github.com/demo/project/pull/88",
            }
        ],
        "metadata": {
            "open_issues_count": 5,
            "open_prs_count": 1,
            "note": "Demo data used because the repository had no open issues/PRs.",
        },
    }

    out_path = Path("data/project_data.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(data, indent=2))
    print(f"Demo data written → {out_path}")
    return data


if __name__ == "__main__":
    collect()
