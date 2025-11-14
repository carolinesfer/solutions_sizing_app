# Tests Directory

This directory contains all testing files and documentation for the Agentic Professional Services Scoper.

## Files

- **`test_all_agents.py`** - Comprehensive Python test script that tests all 4 agents in sequence with full validation
- **`test_agents.sh`** - Quick shell script for CLI-based testing of individual agents
- **`TESTING.md`** - Complete testing guide with all methods, expected outputs, and troubleshooting
- **`TEST_FILES_EXPLANATION.md`** - Explanation of test file consolidation and structure

## Quick Start

### Run All Tests (Recommended)
```bash
cd tests
PYTHONPATH=.. python test_all_agents.py
```

### Quick CLI Tests
```bash
./tests/test_agents.sh
```

For detailed information, see [TESTING.md](./TESTING.md).

