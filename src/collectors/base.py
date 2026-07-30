"""
Base interface for all data collectors.

Any new tool (Jira, Linear, Notion, etc.) should implement this interface
so the rest of the system stays unchanged.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseCollector(ABC):
    """Standard interface every collector must follow."""

    @abstractmethod
    def collect(self) -> Dict[str, Any]:
        """
        Collect project data and return it in the standard format:

        {
            "source": "github" | "jira" | "linear" | "notion",
            "collected_at": "ISO timestamp",
            "issues": [ ... ],
            "pull_requests": [ ... ],        # optional
            "metadata": { ... }              # optional extra context
        }
        """
        pass

    def normalize_issue(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        """Helper to convert tool-specific issue format into a common shape."""
        return {
            "id": raw.get("id") or raw.get("key"),
            "title": raw.get("title") or raw.get("summary"),
            "state": raw.get("state") or raw.get("status"),
            "labels": raw.get("labels", []),
            "assignees": raw.get("assignees", []),
            "created_at": raw.get("created_at"),
            "updated_at": raw.get("updated_at"),
            "due_date": raw.get("due_date") or raw.get("duedate"),
            "body": raw.get("body") or raw.get("description", ""),
            "comments_count": raw.get("comments_count", 0),
            "url": raw.get("url") or raw.get("html_url"),
        }
