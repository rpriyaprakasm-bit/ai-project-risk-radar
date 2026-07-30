"""
Stub for future Jira collector.
Implement the same interface as BaseCollector / github_collector.
"""

from typing import Any, Dict
from ..base import BaseCollector


class JiraCollector(BaseCollector):
    def collect(self) -> Dict[str, Any]:
        raise NotImplementedError(
            "Jira collector not implemented yet. "
            "See docs/extending.md for the expected data format."
        )
