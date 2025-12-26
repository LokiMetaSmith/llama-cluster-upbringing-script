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
# STATUS LOGIC
# ==========================================
check_status() {
    echo "--- Agentic Workflow Status ---"
    if ! command -v gh &> /dev/null; then
        echo "❌ Error: 'gh' CLI not found. Status check requires GitHub CLI."
        return 1
    fi

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
# Agentic Validation Loop Architecture (Isolated & Recursive)

This repository uses a "Validation Loop" to bridge AI agents with local workstation hardware via an isolated container environment.

## 1. The Architecture
- **Step A (Agent Implementation):** The agent (Jules) pushes code changes and a **new follow-up task** in `ISSUES/`.
- **Step B (Remote Verification):** `remote-verify.yml` triggers on the **Self-Hosted Runner**.
- **Step C (Isolated Execution):** The workstation runs `./bootstrap.sh --container --debug`, generating `playbook_output.log`.
- **Step D (Log Evaluation):** `jules-queue.yml` inspects logs. If Ansible errors exist, it blocks the queue and notifies the agent.
- **Step E (Continuous Motion):** `auto-merge.yml` blocks merges unless a new follow-up issue is detected in the PR.

## 2. Requirements
- **GitHub Self-Hosted Runner:** Must be installed and tagged `self-hosted` on the workstation.
- **Secret `IMPERSONATION_PAT`:** PAT with `repo` and `workflow` scopes.
- **Isolation:** All code executes inside the `pipecat-dev-container` to protect the host machine.
EOF

    echo "[5/6] Writing workflow files..."

    # --- WORKFLOW: CREATE ISSUES ---
    cat <<'EOF' > .github/workflows/create-issues-from-files.yml
name: Create Issues from Files
on:
  workflow_dispatch:
  push: { paths: ["ISSUES/**", "issues/**"] }
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
          gh issue list --label "auto-generated" --state all --limit 1000 --json title --jq '.[].title' > existing_titles.txt
          files=$(find ISSUES issues -maxdepth 1 -name "*.md" -type f 2>/dev/null | sort -V || true)
          for file in $files; do
            expected_title="Issue for $(basename "$file")"
            grep -Fxq "$expected_title" existing_titles.txt && continue
            body_file=$(mktemp)
            { echo "Automatically created for: \`$file\`"; echo "### Content"; echo '```'; cat "$file"; echo '```'; echo "---"; echo "### Directive: Recursive Task Generation"; echo "This system requires constant evolution. This task must generate a successor."; } > "$body_file"
            gh issue create --title "$expected_title" --body-file "$body_file" --label "auto-generated"
          done
EOF

    # --- WORKFLOW: QUEUE MANAGER ---
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

      - name: Evaluate Playbook Logs
        run: |
          RUN_ID=$(gh run list --workflow "Remote Verification" --limit 1 --json databaseId -q '.[0].databaseId')
          if [ -n "$RUN_ID" ]; then
            gh run download "$RUN_ID" --name execution-logs --dir ./remote_logs || true
            if [ -f "./remote_logs/playbook_output.log" ]; then
              if grep -Ei "failed=[1-9]|unreachable=[1-9]|DEPLOYMENT_FAILED" ./remote_logs/playbook_output.log > /dev/null; then
                ISSUE_NUM=$(gh issue list --label "jules" --state open --json number -q '.[0].number')
                gh issue comment "$ISSUE_NUM" --body "### ❌ Cluster Playbook Failed\nErrors detected in isolated run:\n\`\`\`text\n$(tail -n 25 ./remote_logs/playbook_output.log)\n\`\`\`"
                exit 1
              fi
            fi
          fi
      - name: Promote Next
        run: |
          next=$(gh issue list --state open --json number --jq 'min_by(.number).number')
          [ -n "$next" ] && gh issue edit "$next" --add-label "jules"
EOF

    # --- WORKFLOW: REMOTE VERIFY (Isolated Container) ---
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
          # Using container isolation for security
          ./bootstrap.sh --container --debug --run-local --tags "app,verification" || {
            echo "DEPLOYMENT_FAILED" >> playbook_output.log
            exit 1
          }
      - name: Upload Native Logs
        if: always()
        uses: actions/upload-artifact@v4
        with: { name: execution-logs, path: playbook_output.log }
EOF

    # --- WORKFLOW: AUTO MERGE (High Entropy Logic) ---
    cat <<'EOF' > .github/workflows/auto-merge.yml
name: Auto Merge and Close
on:
  workflow_run:
    workflows: ["Remote Verification"]
    types: [completed]
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

          # Check for new issues in this PR (The Entropy Check)
          if gh pr diff "$PR_URL" --name-only | grep -Ei "^(ISSUES|issues)/"; then
            echo "[SUCCESS] Follow-up task detected."
            gh pr merge --merge "$PR_URL"
            PR_BODY=$(gh pr view "$PR_URL" --json body -q .body)
            ISSUE_NUM=$(echo "$PR_BODY" | grep -oEi '(close|closes|closed|fix|fixes|fixed) #[0-9]+' | grep -oE '[0-9]+' | head -n 1)
            [ -n "$ISSUE_NUM" ] && gh issue close "$ISSUE_NUM" --comment "Auto-closed via validation loop."
          else
            echo "[FAILURE] No follow-up issue found."
            gh pr comment "$PR_URL" --body "**[FAILURE] Entropy Detected**: This PR does not include a new task in \`ISSUES/\`. Blocks merge."
            exit 1
          fi
EOF

    echo "[6/6] Setup Complete! Next steps:"
    echo "1. git add . && git commit -m 'chore: setup isolated agentic loop' && git push"
    echo "2. Add secret IMPERSONATION_PAT to GitHub Repo Settings."
    echo "3. Run: ./agentic_workflow.sh --ignite"
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
        --body "### Mission: Initialize Cluster Upbringing (Isolated Loop)
- Verify bootstrap.sh --container logic works on the hardware runner.
- Confirm folder structure (src/, tests/, ISSUES/).
- Generate the next task file in ISSUES/ for core services."
    echo "✅ Project ignited. Automation engine is live."
}

# ==========================================
# UNINSTALL LOGIC
# ==========================================
uninstall_workflow() {
    echo "Cleaning config..."
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
