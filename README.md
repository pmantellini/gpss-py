gpss-py
=======

Experimental (work-in-progress) Python interpreter / runtime skeleton for a GPSS-like discrete event simulation language.

Status: Prototype. Core mechanics are intentionally minimal; many GPSS concepts are not yet implemented. See Roadmap below.

## Features (current)
- Basic System, SubSystem, Transaction skeletons
- Block types: Generate (periodic / capped), Advance (fixed delay), Terminate (count-based)
- Current Events Chain (CEC) & Future Events Chain (FEC) minimal handling
- Simple discrete clock tick loop with safety max tick cap
- Basic unit tests for blocks and system creation

## Not Yet Implemented / Partial
(Full detail in `ROADMAP.md`)
- Time jump to next event (clock currently increments by 1)
- Random sampling using med/deviation operands
- Priority handling & stable ordering rules
- Rich GPSS blocks (QUEUE, DEPART, SEIZE, RELEASE, STORAGE, etc.)
- Statistics collection & reporting
- Robust termination criteria (time limit, total terminations) beyond Terminate block count
- Resource modeling, queues, utilization metrics
- Logging / tracing layer
- Configuration & seeding for reproducibility
- CLI / script parser for GPSS-like input language

## Installation (development)
Clone the repository and install in editable mode:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Quick Start
```python
from GPSS import System, SubSystem
from blocks import Generate, Advance, Terminate

# Create blocks: generate 3 transactions (first at time 0, then every 5 ticks),
# each advances 3 ticks, then terminates after 3 completions.
g = Generate(med_value=5, first_tx=0, max_amount=3)
a = Advance(max_value=3)
t = Terminate(amount=3)

sub = SubSystem()
sub.addBlock(g)
sub.addBlock(a)
sub.addBlock(t)

system = System()
system.addSubSystem(sub)
system.runSimulation()
```
Current behavior: clock increases one tick at a time; Generate spawns transactions at scheduled ticks; Advance delays transactions by fixed amount; Terminate counts completions until amount met.

## Running Tests
```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

## Project Structure
```
GPSS.py      # Core System, Scheduler, Transaction, SubSystem
blocks.py    # Block base + Generate, Advance, Terminate
chains.py    # CurrentEventsChain & FutureEventsChain
tests/       # Unit tests
pyproject.toml
```

## Design Notes
The architecture follows classic GPSS concepts:
- Transactions flow through a sequence of blocks.
- Generate/Advance can schedule (delay) transactions onto the Future Events Chain.
- Scheduler moves due transactions to the Current Events Chain and processes them.

Simplifications for now:
- No heap/priority queue; simple lists are used.
- Delays are deterministic; deviation ignored.
- No statistical collection or resource contention constructs yet.

## Roadmap
See `ROADMAP.md` for detailed tasks and priorities.

## Contributing
See `CONTRIBUTING.md` for guidelines (development environment, branching, commit style, testing). Please add or update tests with any behavior change.

We follow a simple Code of Conduct (see `CODE_OF_CONDUCT.md`).

## License
MIT (see `LICENSE`).

## Disclaimer
Not production ready. Interfaces may change frequently while core semantics are fleshed out.

