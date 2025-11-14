# Test Files Explanation

This document explains the consolidated test files for the Agentic Professional Services Scoper.

## Consolidated Structure

After consolidation, we now have **3 main files** instead of 8+ redundant ones:

### 1. `test_all_agents.py` - Main Python Test Script

**Purpose:** Comprehensive testing of all 4 agents in sequence with validation

**Usage:**
```bash
cd tests
PYTHONPATH=.. python test_all_agents.py
```

**Features:**
- Tests all 4 agents in workflow order (Requirement Analyzer → Questionnaire → Clarifier → Architecture)
- Validates each agent's output schema
- Passes output from one agent as input to the next
- Shows formatted, readable results
- Provides summary at the end
- Checks for DataRobot credentials before running

**When to use:**
- Full integration testing
- Validating the complete workflow
- Debugging agent interactions
- CI/CD pipelines

### 2. `test_agents.sh` - Quick CLI Test Script

**Purpose:** Fast testing of each agent individually via CLI

**Usage:**
```bash
./tests/test_agents.sh
# Or from tests directory:
cd tests && ./test_agents.sh
```

**Features:**
- Tests each agent independently via `task cli`
- Non-interactive (good for automation)
- Shows last 50 lines of output per test
- Continues even if one test fails
- Simple shell script, no dependencies

**When to use:**
- Quick smoke tests
- Testing individual agents in isolation
- When you don't need full workflow validation
- CI/CD quick checks

### 3. `TESTING.md` - Consolidated Documentation

**Purpose:** Single source of truth for all testing information

**Contents:**
- Prerequisites and setup
- All testing methods explained
- Expected outputs for each agent
- Troubleshooting guide
- Next steps after testing

**When to use:**
- First-time setup
- Understanding what each test does
- Troubleshooting issues
- Reference for testing procedures

## What Was Removed

The following redundant files were consolidated:

1. **`test_agent_direct.py`** - Redundant with `test_all_agents.py`
2. **`test_agents_locally.sh`** - Redundant with `test_agents.sh` (interactive version wasn't needed)
3. **`test_agents_simple.sh`** - Redundant with `test_agents.sh`
4. **`test_all_agents.sh`** - Redundant with `test_agents.sh`
5. **`test_agents_via_api.py`** - Not needed (CLI testing is simpler)
6. **`README_TESTING.md`** - Merged into `TESTING.md`
7. **`TEST_AGENTS_GUIDE.md`** - Merged into `TESTING.md`
8. **`requirement_analyzer_agent/test_direct.py`** - Redundant with `test_all_agents.py`

## Testing Workflow

### Recommended Testing Flow

1. **First Time Setup:**
   - Read `TESTING.md` for prerequisites
   - Set up DataRobot credentials or OpenAI API key
   - Ensure `INFRA_ENABLE_LLM=gateway_direct.py` is in `.env`

2. **Quick Test:**
   ```bash
   ./tests/test_agents.sh
   ```
   This verifies each agent can run independently.

3. **Full Integration Test:**
   ```bash
   cd tests
   PYTHONPATH=.. python test_all_agents.py
   ```
   This tests the complete workflow end-to-end.

4. **Individual Agent Testing:**
   Use the commands in `TESTING.md` Method 3 to test specific agents.

## Key Differences

| Feature | `test_all_agents.py` | `test_agents.sh` |
|---------|---------------------|------------------|
| **Type** | Python script | Shell script |
| **Testing** | Direct agent calls | Via CLI (`task cli`) |
| **Validation** | Full schema validation | Output inspection |
| **Workflow** | Sequential (passes data) | Independent tests |
| **Dependencies** | Python, all agent deps | Just `task` command |
| **Output** | Formatted, detailed | Last 50 lines |
| **Best For** | Integration testing | Quick smoke tests |

## Migration Guide

If you were using the old files:

- **`test_agents_locally.sh`** → Use `test_agents.sh` (same functionality, no interactive prompts)
- **`test_agents_simple.sh`** → Use `test_agents.sh` (identical)
- **`test_all_agents.sh`** → Use `test_agents.sh` (same approach)
- **`test_agent_direct.py`** → Use `test_all_agents.py` (includes this functionality)
- **`README_TESTING.md` or `TEST_AGENTS_GUIDE.md`** → Use `TESTING.md` (consolidated)

## Summary

**Before:** 8+ test files with overlapping functionality scattered across the repository  
**After:** 4 focused files in `tests/` directory:
- `tests/test_all_agents.py` - Comprehensive Python testing
- `tests/test_agents.sh` - Quick CLI testing  
- `tests/TESTING.md` - Complete documentation
- `tests/TEST_FILES_EXPLANATION.md` - This file (explanation of consolidation)

This consolidation makes testing simpler, clearer, and easier to maintain. All testing files are now organized in a single `tests/` directory at the repository root.

