from __future__ import annotations

from dataclasses import dataclass, field

from verifai.core.services.base import AgentService
from verifai.utils.json_extract import extract_json_object


@dataclass(frozen=True)
class LogFailure:
    signal: str
    category: str
    description: str
    suggested_probe: str


@dataclass(frozen=True)
class LogTriageResult:
    summary: str
    failures: list[LogFailure] = field(default_factory=list)
    raw_response: str = ""


class LogTriage(AgentService):
    """Parses simulation log output to flag and categorize likely failure causes."""

    system_prompt = (
        "You are a senior hardware verification engineer triaging simulation logs. "
        "Given raw simulation output, identify each distinct failure, categorize its "
        "likely root cause (e.g. timing, protocol violation, reset issue, randomization "
        "corner case, testbench bug), and suggest which signals to probe next. Respond "
        "with ONLY a JSON object matching this schema, no prose, no code fences:\n"
        '{"summary": "<one paragraph summary>", "failures": ['
        '{"signal": "<primary signal involved, or empty string>", '
        '"category": "<likely root cause category>", "description": "<what happened>", '
        '"suggested_probe": "<what to probe next>"}]}'
    )

    def triage(self, simulation_log: str) -> LogTriageResult:
        if not simulation_log.strip():
            raise ValueError("simulation_log must not be empty")

        response = self._ask(f"Simulation log:\n\n{simulation_log}")
        data = extract_json_object(response)
        failures = [
            LogFailure(
                signal=item.get("signal", ""),
                category=item.get("category", "unknown"),
                description=item.get("description", ""),
                suggested_probe=item.get("suggested_probe", ""),
            )
            for item in data.get("failures", [])
        ]
        return LogTriageResult(summary=data.get("summary", ""), failures=failures, raw_response=response)
