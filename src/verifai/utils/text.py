from __future__ import annotations

import re

_FENCE_RE = re.compile(r"^```[a-zA-Z0-9_+-]*\n(.*)\n```$", re.DOTALL)


def strip_code_fence(text: str) -> str:
    """Strip a single leading/trailing markdown code fence, if present."""
    stripped = text.strip()
    match = _FENCE_RE.match(stripped)
    return match.group(1).strip() if match else stripped
