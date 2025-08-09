# gpss-py Roadmap

This document tracks remaining and planned work. Items are grouped by phase.

Legend: P1 = high priority (next), P2 = medium, P3 = later / stretch.

## Phase 1: Core Engine Stabilization (P1)
- [ ] Jump clock to next scheduled event time instead of +1 ticks when CEC empty.
- [ ] Refactor Advance to sample delay using med/deviation semantics (define distribution: e.g. uniform around med ± deviation or normal truncated at 0).
- [ ] Implement proper delayed scheduling: Advance should set scheduled_time = current_clock + sampled_delay.
- [ ] Add Transaction priority & sequence index; update CEC ordering accordingly.
- [ ] Replace list-based FEC with a min-heap keyed by (scheduled_time, priority, sequence).
- [ ] Provide explicit termination conditions (e.g., max simulated time, total terminated transactions).
- [ ] Ensure Generate sets transaction scheduled_time = current clock (currently 0) for clarity.
- [ ] Normalize naming to snake_case (public API may need transitional aliases).

## Phase 2: Additional Block Types (P1/P2)
- [ ] QUEUE / DEPART for queue length tracking.
- [ ] SEIZE / RELEASE for Facility (single server) resources.
- [ ] ENTER / LEAVE for STORAGE (multi-unit resource pools).
- [ ] ADVANCE: support min, max operands and random distribution selection.
- [ ] GENERATE: support interarrival distributions (EXPO, ERLA, etc.).

## Phase 3: Resources & Statistics (P2)
- [ ] Facility class with utilization stats (busy time, wait times).
- [ ] Queue statistics: average length, max length, waiting time distribution.
- [ ] Global counters and user-defined variables.
- [ ] Snapshot & time-weighted statistics framework.

## Phase 4: Instrumentation & UX (P2)
- [ ] Logging/tracing with verbosity levels.
- [ ] Deterministic seeding (System(seed=...)).
- [ ] Progress / event audit export (CSV / JSON) for debugging.
- [ ] Basic visual timeline (optional later).

## Phase 5: Configuration & Parsing (P3)
- [ ] Simple DSL or parser for a GPSS-like script -> model objects.
- [ ] CLI entry point (e.g., `gpss-run model.gpss`).

## Phase 6: Testing & Quality (P1/P2)
- [ ] Expand unit tests for scheduler ordering & time skipping.
- [ ] Property-based tests (Hypothesis) for invariants (no negative time, ordering stable).
- [ ] Integration test: multi-customer facility queue scenario.
- [ ] Add linting (Ruff/flake8) & typing (mypy/pyright) CI workflow.
- [ ] Code coverage tracking (coverage.py + badge).

## Phase 7: Documentation (P2)
- [ ] Block API reference (docstrings & generated docs).
- [ ] Examples directory with multiple scenarios.
- [ ] CONTRIBUTING.md & CODE_OF_CONDUCT.md.
- [ ] LICENSE file (MIT text).

## Stretch / Future (P3)
- [ ] Parallel replication runner for variance reduction.
- [ ] Warm-up period detection & truncation.
- [ ] Batch means / statistical output summaries.
- [ ] GUI or notebook widgets for interactive experimentation.
- [ ] Performance optimization (cython / pypy) if needed.

## Completed (keep updated)
- [x] Basic skeleton classes (System, SubSystem, Transaction, Scheduler, Chains).
- [x] Generate / Advance / Terminate minimal implementations.
- [x] Unit tests scaffold.
- [x] README baseline.
- [x] Roadmap document.

---
Contributions: please open an issue referencing roadmap item IDs or propose new items with rationale.
