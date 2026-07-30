"""
Stub for future Linear collector.
"""

from typing import Any, Dict
from ..base import BaseCollector


class LinearCollector(BaseCollector):
    def collect(self) -> Dict[str, Any]:
        raise NotImplementedError(
            "Linear collector not implemented yet. "
            "See docs/extending.md for the expected data format."
        )
