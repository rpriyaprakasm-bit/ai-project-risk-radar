"""
Stub for future Notion collector.
"""

from typing import Any, Dict
from ..base import BaseCollector


class NotionCollector(BaseCollector):
    def collect(self) -> Dict[str, Any]:
        raise NotImplementedError(
            "Notion collector not implemented yet. "
            "See docs/extending.md for the expected data format."
        )
