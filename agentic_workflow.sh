#!/bin/bash

# --- Configuration ---
# Standardizing on ISSUES directory for task generation
ISSUE_DIR="ISSUES"

# --- Help Menu ---
show_help() {
    echo "======================================================"
    echo " Llama-Cluster Agentic Workflow Manager (Jules)"
    echo "======================================================"
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  --setup      Install isolated workflows and 'Continuous Motion' logic."
    echo "  --ignite     Create the first issue to trigger the AI Agent."
    echo "  --status     Check Jules queue state and hardware runner health."
    echo "  --uninstall  Remove all workflow files and clean GitHub labels."
    echo "  --purge      (Used with --uninstall) Also purge Nomad jobs via bootstrap.sh."
    echo "  -h, --help   Display this help message."
}

# --- Initialization ---
ACTION=""
PURGE_NOMAD=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --setup) ACTION="setup" ; shift ;;
        --ignite) ACTION="ignite" ; shift ;;
        --uninstall) ACTION="uninstall" ; shift ;;
        --status) ACTION="status" ; shift ;;
        --purge) PURGE_NOMAD=true ; shift ;;
        -h|--help) show_help ; exit 0 ;;
        *) echo "Unknown option: $1" ; show_help ; exit 1 ;;
    esac
done

if [ -z "$ACTION" ]; then
    show_help
    exit 1
fi

# ==========================================
# STATUS LOGIC (Workstation Dashboard)
# ==========================================
check_status() {
    echo "--- Agentic Workflow Status ---"
    if ! command -v gh &> /dev/null; then
        echo "❌ Error: 'gh' CLI not found. Status check requires GitHub CLI."
        return 1
    fi

    # 1. Fetch active task
    ACTIVE_ISSUE=$(gh issue list --label "jules" --state open --json number,title,updatedAt --jq '.[0]')
    
    if [ -n "$ACTIVE_ISSUE" ] && [ "$ACTIVE_ISSUE" != "null" ]; then
        ISSUE_NUM=$(echo "$ACTIVE_ISSUE" | jq -r '.number')
        ISSUE_TITLE=$(echo "$ACTIVE_ISSUE" | jq -r '.title')
        UPDATED_AT=$(echo "$ACTIVE_ISSUE" | jq -r '.updatedAt')
        
        CURRENT_TS=$(date +%s)
        LAST_TS=$(date -d "$UPDATED_AT" +%s 2>/dev/null || date -j -f "%Y-%m-%dT%H:%M:%SZ" "$UPDATED_AT" +%s)
        DIFF=$((CURRENT_TS - LAST_TS))
        
        echo "📍 Active Task: Issue #$ISSUE_NUM - $ISSUE_TITLE"
        echo "🕒 Last Activity: $((DIFF / 3600))h $(((DIFF % 3600) / 60))m ago"
        
        # Stall threshold is 2 hours (7200s)
        if [ "$DIFF" -gt 7200 ]; then
            echo "⚠️  STATUS: STALLED (Threshold >2h - Verify hardware runner is online)"
        else
            echo "✅ STATUS: ACTIVE"
        fi
    else
        echo "📭 STATUS: IDLE"
    fi

    QUEUE_COUNT=$(gh issue list --state open --limit 100 --json number --jq 'length')
    echo "📊 Queue Depth: $QUEUE_COUNT open issues"
}

# ==========================================
# SETUP LOGIC (The Isolated Loop)
# ==========================================
setup_workflow() {
    echo "[1/6] Validating environment..."
    if ! gh auth status &>/dev/null; then
        echo "❌ Error: Not logged into 'gh' CLI. Run 'gh auth login' first."
        exit 1
    fi

    echo "[2/6] Creating structure..."
    mkdir -p .github/workflows .github/context "$ISSUE_DIR" src tests

    echo "[3/6] Initializing Required GitHub Labels..."
    gh label create "jules" --color "0052cc" --description "Active AI Agent Task" --force || true
    gh label create "auto-generated" --color "ededed" --description "Tasks created from files" --force || true

    echo "[4/6] Generating Architecture Guide..."
    cat <<'EOF' > .github/AGENTIC_README.md
# Agentic Validation Loop Architecture

This repository uses a "Validation Loop" to bridge AI agents with local workstation hardware via isolated containers.

## The Loop
- **Implementation:** Jules (Agent) pushes code and a **successor task** in `ISSUES/`.
- **Remote Verification:** `remote-verify.yml` triggers on the **Self-Hosted Runner**.
- **Execution:** Hardware runs `./bootstrap.sh --container --debug`, generating native `playbook_output.log`.
- **Log Evaluation:** `jules-queue.yml` inspects logs for Ansible failures (`failed=1` or `unreachable=1`).
- **Continuous Motion:** `auto-merge.yml` blocks merges unless a new task definition is detected in the PR diff.
EOF

    echo "[5/6] Writing workflow files..."

    # --- CREATE ISSUES (Duplicate Check & Sorting) ---
    cat <<'EOF' > .github/workflows/create-issues-from-files.yml
name: Create Issues from Files
on:
  workflow_dispatch:
  push: { paths: ["ISSUES/**", "issues/**"] }
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: false
jobs:
  create-issues:
    runs-on: ubuntu-latest
    permissions: { issues: write, contents: read }
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Process
        env: { GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }} }
        run: |
          gh issue list --label "auto-generated" --state all --limit 1000 --json title --jq '.[].title' > existing.txt
          files=$(find ISSUES issues -maxdepth 1 -name "*.md" -type f 2>/dev/null | sort -V || true)
          if [ -z "$files" ]; then exit 0; fi
          while IFS= read -r file; do
              filename=$(basename "$file")
              expected="Issue for $filename"
              if grep -Fxq "$expected" existing.txt; then continue; fi
              body_file=$(mktemp)
              { echo "Auto-created for: \`$file\`"; echo -e "\n### Content\n\`\`\`"; cat "$file"; echo -e "\n\`\`\`\n---\n### Directive: Recursive Task Generation"; echo "Every task MUST generate a successor in ISSUES/ to maintain forward motion."; } > "$body_file"
              gh issue create --title "$expected" --body-file "$body_file" --label "auto-generated"
              sleep 2
          done < <(printf "%s\n" "$files")
EOF

    # --- QUEUE MANAGER (Stall check & native log parser) ---
    cat <<'EOF' > .github/workflows/jules-queue.yml
name: Jules Label Queue
on:
  issues: { types: [opened, labeled, closed, reopened] }
  workflow_run: { workflows: ["Auto Merge and Close"], types: [completed] }
  schedule: [{cron: '0 * * * *'}]
jobs:
  enforce-jules:
    runs-on: ubuntu-latest
    env: { GH_TOKEN: ${{ secrets.IMPERSONATION_PAT }}, MAX_RUNS: ${{ vars.JULES_MAX_DAILY_RUNS || '10' }} }
    steps:
      - name: Rate Limit & Stall Check
        run: |
          SINCE=$(date -u -d '24 hours ago' '+%Y-%m-%dT%H:%M:%SZ')
          RECENT=$(gh search issues --repo "${{ github.repository }}" --label "jules" --updated ">$SINCE" --json number --jq 'length')
          [ "${RECENT:-0}" -ge "$MAX_RUNS" ] && exit 0
          active=$(gh issue list --label "jules" --state open --json number --jq '.[0]')
          [ -n "$active" ] && exit 0

      - name: Evaluate Native Playbook Logs
        run: |
          RUN_ID=$(gh run list --workflow "Remote Verification" --limit 1 --json databaseId -q '.[0].databaseId')
          if [ -n "$RUN_ID" ]; then
            gh run download "$RUN_ID" --name execution-logs --dir ./remote_logs || true
            if [ -f "./remote_logs/playbook_output.log" ] && grep -Ei "failed=[1-9]|unreachable=[1-9]|DEPLOYMENT_FAILED" ./remote_logs/playbook_output.log > /dev/null; then
                ISSUE_NUM=$(gh issue list --label "jules" --state open --json number -q '.[0].number')
                gh issue comment "$ISSUE_NUM" --body "### ❌ Cluster Playbook Failed\nIsolated remote run reported errors:\n\`\`\`text\n$(tail -n 25 ./remote_logs/playbook_output.log)\n\`\`\`"
                exit 1
            fi
          fi
      - name: Promote Next
        run: |
          next=$(gh issue list --state open --json number --jq 'min_by(.number).number')
          [ -n "$next" ] && gh issue edit "$next" --add-label "jules"
EOF

    # --- REMOTE VERIFY (Isolated Cluster Execution) ---
    cat <<'EOF' > .github/workflows/remote-verify.yml
name: Remote Verification
on:
  pull_request: { types: [opened, synchronize, ready_for_review] }
jobs:
  verify-on-workstation:
    runs-on: self-hosted
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Run Isolated Cluster Upbringing
        run: |
          chmod +x ./bootstrap.sh
          # Executes inside pipecat-dev-container for safety
          ./bootstrap.sh --container --debug --run-local --tags "app,verification" || { echo "DEPLOYMENT_FAILED" >> playbook_output.log; exit 1; }
      - name: Upload Logs
        if: always()
        uses: actions/upload-artifact@v4
        with: { name: execution-logs, path: playbook_output.log }
EOF

    # --- AUTO MERGE (High Entropy Enforcement) ---
    cat <<'EOF' > .github/workflows/auto-merge.yml
name: Auto Merge and Close
on:
  workflow_run: { workflows: ["Remote Verification"], types: [completed] }
permissions: { contents: write, pull-requests: write, issues: write }
jobs:
  merge-and-close:
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Verify Motion and Merge
        env: { GH_TOKEN: ${{ secrets.IMPERSONATION_PAT }}, HEAD_BRANCH: ${{ github.event.workflow_run.head_branch }}, REPO: ${{ github.repository }} }
        run: |
          PR_URL=$(gh pr list --repo "$REPO" --head "$HEAD_BRANCH" --state open --json url --jq '.[0].url')
          if [ -z "$PR_URL" ]; then exit 0; fi
          if gh pr diff "$PR_URL" --name-only | grep -Ei "^(ISSUES|issues)/"; then
            gh pr merge --merge "$PR_URL"
            ISSUE_NUM=$(gh pr view "$PR_URL" --json body -q .body | grep -oEi '(close|closes|closed|fix|fixes|fixed) #[0-9]+' | grep -oE '[0-9]+' | head -n 1)
            [ -n "$ISSUE_NUM" ] && gh issue close "$ISSUE_NUM" --comment "Auto-closed via validation loop."
          else
            gh pr comment "$PR_URL" --body "**[FAILURE] Entropy Detected**: This PR lacks a successor task in \`ISSUES/\`."
            exit 1
          fi
EOF

    echo "[6/6] Setup Complete! Next: push changes and run --ignite."
}

# ==========================================
# IGNITE LOGIC
# ==========================================
ignite_workflow() {
    echo "🚀 Starting Project Ignition..."
    REPO_NAME=$(basename "$(pwd)")
    gh issue create \
        --title "Scaffold: Initialize $REPO_NAME" \
        --label "jules" \
        --body "### Mission: Initialize Isolated Loop
- Verify bootstrap.sh --container functionality on host.
- Establish follow-up task sequence in ISSUES/.
- Ensure continuous motion by requiring successors for every PR."
}

# ==========================================
# UNINSTALL LOGIC
# ==========================================
uninstall_workflow() {
    echo "Removing configs..."
    rm -f .github/workflows/*.yml .github/AGENTIC_README.md
    rm -rf .github/context/ "$ISSUE_DIR"/
    gh label delete "jules" --yes || true
    gh label delete "auto-generated" --yes || true
    if [ "$PURGE_NOMAD" = true ] && [ -f "./bootstrap.sh" ]; then
        ./bootstrap.sh --purge-jobs
    fi
    echo "✅ Agentic workflow removed."
}

# --- Router ---
if [ "$ACTION" == "setup" ]; then setup_workflow;
elif [ "$ACTION" == "ignite" ]; then ignite_workflow;
elif [ "$ACTION" == "uninstall" ]; then uninstall_workflow;
elif [ "$ACTION" == "status" ]; then check_status; fi
