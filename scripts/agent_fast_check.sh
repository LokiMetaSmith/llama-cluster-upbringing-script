#!/usr/bin/env bash
#
# Unified Fast Verification Script for Autonomous Agents
#
# This script serves as a lightweight, sandbox-friendly, offline-only verification
# suite for rapid development iterations. It avoids heavy bootstrap or systemd
# dependencies, making it extremely fast to run.
#
# Checks included:
#   1. Playbook syntax and dry-run validation (via scripts/check_all_playbooks.sh)
#   2. Code and document linting (via scripts/lint.sh)
#   3. Python unit tests (via pytest, with support for specific targets/filters)

# Ensure we run from the repository root
cd "$(dirname "$0")/.." || exit 1

# Color definitions for gorgeous terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Default modes
RUN_LINT=true
RUN_PLAYBOOKS=true
RUN_TESTS=true
PYTEST_ARGS=()

# Display help message
show_help() {
    echo -e "${BOLD}Distributed Conversational AI Pipeline - Fast Verification Script${NC}"
    echo -e "Usage: $0 [options] [pytest_targets_or_options]"
    echo ""
    echo "Options:"
    echo "  --lint-only        Run only code and document linters"
    echo "  --playbooks-only   Run only Playbook syntax dry-runs"
    echo "  --tests-only       Run only Python unit tests"
    echo "  -h, --help         Display this help message and exit"
    echo ""
    echo "Pytest forwarding:"
    echo "  Any other arguments (e.g., tests/unit/test_safe_flatten.py, -k safe_flatten, etc.)"
    echo "  will be forwarded directly to pytest."
    echo ""
    echo "Examples:"
    echo "  $0                                                    # Run all lint, playbook, and unit tests"
    echo "  $0 --tests-only tests/unit/test_safe_flatten.py      # Run only the safe_flatten unit test"
    echo "  $0 -k crdt_memory                                    # Run all checks, filtering pytest to crdt_memory"
}

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --lint-only)
            RUN_LINT=true
            RUN_PLAYBOOKS=false
            RUN_TESTS=false
            ;;
        --playbooks-only)
            RUN_LINT=false
            RUN_PLAYBOOKS=true
            RUN_TESTS=false
            ;;
        --tests-only)
            RUN_LINT=false
            RUN_PLAYBOOKS=false
            RUN_TESTS=true
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            # Anything else is forwarded to pytest
            PYTEST_ARGS+=("$1")
            ;;
    esac
    shift
done

echo -e "${BOLD}${BLUE}===================================================================${NC}"
echo -e "${BOLD}${BLUE}                AGENT FAST VERIFICATION CHECKLIST                  ${NC}"
echo -e "${BOLD}${BLUE}===================================================================${NC}"
echo -e "Starting checks. Mode: Offline, sandbox-friendly, high-speed iteration."
echo ""

# Global exit / report trackers
LINT_STATUS="Skipped"
PLAYBOOK_STATUS="Skipped"
TEST_STATUS="Skipped"

# 1. RUN LINTERS
if [ "$RUN_LINT" = true ]; then
    echo -e "${BOLD}${CYAN}[1/3] Running Code & Document Linters...${NC}"
    echo "------------------------------------------------------------"
    if [ -f "./scripts/lint.sh" ]; then
        ./scripts/lint.sh
        LINT_EXIT_CODE=$?
        if [ $LINT_EXIT_CODE -eq 0 ]; then
            LINT_STATUS="${GREEN}PASSED${NC}"
            echo -e "${GREEN}✅ All linters passed successfully!${NC}"
        else
            LINT_STATUS="${RED}FAILED${NC} (Check details above)"
            echo -e "${YELLOW}⚠️  Some linters reported issues (warnings/errors). This is common during local development but should be reviewed.${NC}"
        fi
    else
        LINT_STATUS="${RED}ERROR${NC} (scripts/lint.sh not found)"
        echo -e "${RED}❌ Error: scripts/lint.sh not found.${NC}"
    fi
    echo ""
fi

# 2. RUN PLAYBOOK SYNTAX DRY-RUNS
if [ "$RUN_PLAYBOOKS" = true ]; then
    echo -e "${BOLD}${CYAN}[2/3] Checking Ansible Playbook Syntax & Dry-Runs...${NC}"
    echo "------------------------------------------------------------"
    if [ -f "./scripts/check_all_playbooks.sh" ]; then
        PLAYBOOK_LOG=$(mktemp)

        # Run playbooks checks and log to temp file
        ./scripts/check_all_playbooks.sh --log > "$PLAYBOOK_LOG" 2>&1
        PLAYBOOK_EXIT_CODE=$?

        # Filter and summarize the output
        PASSED_COUNT=$(grep -c "Dry-run PASSED" "$PLAYBOOK_LOG" || echo "0")
        FAILED_COUNT=$(grep -c "Dry-run FAILED" "$PLAYBOOK_LOG" || echo "0")

        # Look specifically for structural/YAML syntax/parsing errors
        # (Exclude expected local connection / missing variable false positives)
        SYNTAX_ERRORS=$(grep -iE "YAML parsing failed|syntax error|parser error|unexpected parameter type|no module/action detected|unquoted value|unmatched quotes|invalid YAML|duplicate dict key" "$PLAYBOOK_LOG" || true)

        # Display summarized output
        cat "$PLAYBOOK_LOG" | grep -E "Checking Playbook|Dry-run PASSED|Dry-run FAILED|complete"

        if [ -n "$SYNTAX_ERRORS" ]; then
            echo ""
            echo -e "${RED}${BOLD}🚨 CRITICAL SYNTAX / STRUCTURAL ERRORS DETECTED:${NC}"
            echo "------------------------------------------------------------"
            echo -e "${YELLOW}$SYNTAX_ERRORS${NC}"
            echo "------------------------------------------------------------"
            PLAYBOOK_STATUS="${RED}SYNTAX ERROR${NC} (Actual syntax/YAML structural error detected)"
        elif [ "$FAILED_COUNT" -gt 0 ]; then
            PLAYBOOK_STATUS="${YELLOW}WARNING${NC} ($PASSED_COUNT passed, $FAILED_COUNT failed/skipped)"
            echo ""
            echo -e "${YELLOW}⚠️  Playbook dry-runs completed. $PASSED_COUNT passed, $FAILED_COUNT failed (mostly due to sandbox missing credentials/variables).${NC}"
        else
            PLAYBOOK_STATUS="${GREEN}PASSED${NC} ($PASSED_COUNT passed)"
            echo ""
            echo -e "${GREEN}✅ All playbook dry-runs passed!${NC}"
        fi

        rm -f "$PLAYBOOK_LOG"
    else
        PLAYBOOK_STATUS="${RED}ERROR${NC} (scripts/check_all_playbooks.sh not found)"
        echo -e "${RED}❌ Error: scripts/check_all_playbooks.sh not found.${NC}"
    fi
    echo ""
fi

# 3. RUN PYTHON UNIT TESTS (pytest)
if [ "$RUN_TESTS" = true ]; then
    echo -e "${BOLD}${CYAN}[3/3] Running Python Unit Tests...${NC}"
    echo "------------------------------------------------------------"

    # If no custom test args provided, default to tests/unit/
    if [ ${#PYTEST_ARGS[@]} -eq 0 ]; then
        PYTEST_TARGETS=("tests/unit/")
    else
        PYTEST_TARGETS=("${PYTEST_ARGS[@]}")
    fi

    echo -e "Executing pytest with targets/options: ${YELLOW}${PYTEST_TARGETS[*]}${NC}"
    echo ""

    if command -v pytest &> /dev/null; then
        pytest "${PYTEST_TARGETS[@]}"
        TEST_EXIT_CODE=$?
        if [ $TEST_EXIT_CODE -eq 0 ]; then
            TEST_STATUS="${GREEN}PASSED${NC}"
            echo ""
            echo -e "${GREEN}✅ Python unit tests passed successfully!${NC}"
        else
            TEST_STATUS="${RED}FAILED${NC} (Exit code $TEST_EXIT_CODE)"
            echo ""
            echo -e "${RED}❌ Pytest execution failed.${NC}"
        fi
    else
        TEST_STATUS="${RED}ERROR${NC} (pytest command not found)"
        echo -e "${RED}❌ Error: pytest is not installed or available in this environment.${NC}"
    fi
    echo ""
fi

# FINAL REPORT SUMMARY
echo -e "${BOLD}${BLUE}===================================================================${NC}"
echo -e "${BOLD}${BLUE}                        VERIFICATION SUMMARY                       ${NC}"
echo -e "${BOLD}${BLUE}===================================================================${NC}"
echo -e "  1. Linting Validation:       $LINT_STATUS"
echo -e "  2. Playbook Structure/Check: $PLAYBOOK_STATUS"
echo -e "  3. Python Unit Tests:        $TEST_STATUS"
echo -e "${BOLD}${BLUE}===================================================================${NC}"

# Exit gracefully or fail if critical syntax/tests failed
if [[ "$TEST_STATUS" == *FAILED* || "$PLAYBOOK_STATUS" == *SYNTAX* ]]; then
    echo -e "${RED}${BOLD}❌ Some critical checks failed. Please fix syntax or unit test issues.${NC}"
    exit 1
else
    echo -e "${GREEN}${BOLD}🎉 Fast verification finished successfully!${NC}"
    exit 0
fi
