from __future__ import annotations

import json
import re
from typing import Any

_FENCE_RE = re.compile(r"```(?:json)?\s*\n?(.*?)\n?```", re.DOTALL)


class JsonExtractionError(ValueError):
    """Raised when a JSON object cannot be extracted from model output."""


def extract_json_object(text: str) -> dict[str, Any]:
    """Extract and parse a JSON object from a model response.

    Handles responses that are pure JSON, JSON wrapped in a markdown code
    fence, or JSON surrounded by incidental prose.
    """
    candidates = [text.strip()]

    fence_match = _FENCE_RE.search(text)
    if fence_match:
        candidates.insert(0, fence_match.group(1).strip())

    for candidate in candidates:
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            continue

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start : end + 1])
        except json.JSONDecodeError:
            pass

    raise JsonExtractionError(f"Could not extract JSON object from response: {text[:200]!r}")
