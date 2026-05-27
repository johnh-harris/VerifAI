# VerifAI

AI-powered assistant for hardware verification — generates testbenches, writes SVA assertions, and analyzes coverage gaps from natural language specs.

## What it does

- **Testbench Generation** — Provide a Verilog/SystemVerilog module and get a UVM-compatible testbench scaffold, including stimulus, checkers, and coverage groups.
- **SVA Assertion Writing** — Describe a protocol or design behavior in plain English and receive synthesizable SystemVerilog Assertions.
- **Coverage Gap Analysis** — Feed in a coverage report and get suggestions for which corner cases are underrepresented and what directed tests might close them.
- **Simulation Log Triage** — Parse simulation output to flag failures, categorize likely causes, and suggest which signals to probe.

## License

MIT

---

Built by John Harris
