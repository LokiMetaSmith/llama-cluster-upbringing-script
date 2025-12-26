#!/bin/bash

# --- Configuration & Metadata ---
REPO_FULL_NAME=$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null)

# --- Help Menu ---
show_help() {
    echo "======================================================"
    echo " Llama-Cluster Agentic Workflow Manager (Jules)"
    echo "======================================================"
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  --setup      Install robust workflows with CONTAINER ISOLATION."
    echo "  --ignite     Create the first issue to trigger the AI Agent."
    echo "  --status     Check Jules queue state and hardware stall detection."
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
            echo "⚠️  STATUS: STALLED (No activity for >2 hours - Check hardware runner)"
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
# SETUP LOGIC (Now with Containerized Verification)
# ==========================================
setup_workflow() {
    echo "[1/5] Checking GitHub CLI Auth..."
    if ! gh auth status &>/dev/null; then
        echo "❌ Error: Not logged into 'gh' CLI. Run 'gh auth login' first."
        exit 1
    fi

    echo "[2/5] Creating structure..."
    mkdir -p .github/workflows .github/context ISSUES src tests

    echo "[3/5] Initializing REQUIRED GitHub Labels..."
    gh label create "jules" --color "0052cc" --description "Active AI Agent Task" --force || true
    gh label create "auto-generated" --color "ededed" --description "Tasks created from files" --force || true

    echo "[4/5] Generating Workflows & Architecture Docs..."

    # --- ARCHITECTURE DOC ---
    cat <<'EOF' > .github/AGENTIC_README.md
# Agentic Validation Loop Architecture (CONTAINERIZED)

This repository uses a "Validation Loop" to bridge AI agents with local workstation hardware via an isolated container environment.

## The Loop
1. **Agent Implementation:** Jules pushes code changes to a branch.
2. **Remote Verification:** The `remote-verify.yml` workflow triggers on a **Self-Hosted Runner**.
3. **ISOLATED Execution:** The workstation runs `./bootstrap.sh --container --debug`, spawning a privileged Docker container.
4. **Log Evaluation:** `jules-queue.yml` inspects logs generated inside the container.
5. **Auto-Merge:** Once logs are clean and checks pass, `auto-merge.yml` merges the PR and closes the task.

## Security & Isolation
- **Containerization:** By using the `--container` flag, Ansible playbooks run within `pipecat-dev-container`.
- **Host Safety:** The agent cannot modify host system files outside the repository volume mapping.
EOF

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
            { echo "Automatically created for: \`$file\`"; echo "### Content"; echo '```'; cat "$file"; echo '```'; echo "---"; echo "### Directive: Recursive Task Generation"; echo "Every task MUST generate at least one follow-up file in ISSUES/."; } > "$body_file"
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
          [ "${RECENT:-0}" -ge "$MAX_RUNS" ] && echo "Limit reached" && exit 0
          active=$(gh issue list --label "jules" --state open --json number --jq '.[0]')
          [ -n "$active" ] && exit 0

      - name: Evaluate Native Playbook Logs
        run: |
          RUN_ID=$(gh run list --workflow "Remote Verification" --limit 1 --json databaseId -q '.[0].databaseId')
          if [ -n "$RUN_ID" ]; then
            gh run download "$RUN_ID" --name execution-logs --dir ./remote_logs || true
            if [ -f "./remote_logs/playbook_output.log" ]; then
              if grep -Ei "failed=[1-9]|unreachable=[1-9]|DEPLOYMENT_FAILED" ./remote_logs/playbook_output.log > /dev/null; then
                ISSUE_NUM=$(gh issue list --label "jules" --state open --json number -q '.[0].number')
                gh issue comment "$ISSUE_NUM" --body "### ❌ Isolated Remote Run Failed\nHardware reported an error inside the container:\n\`\`\`text\n$(tail -n 25 ./remote_logs/playbook_output.log)\n\`\`\`"
                exit 1
              fi
            fi
          fi
      - name: Promote Next
        run: |
          next=$(gh issue list --state open --json number --jq 'min_by(.number).number')
          [ -n "$next" ] && gh issue edit "$next" --add-label "jules"
EOF

    # --- WORKFLOW: REMOTE VERIFY (CONTAINERIZED) ---
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
          # Added --container for isolation
          ./bootstrap.sh --container --debug --run-local --tags "app,verification" || {
            echo "DEPLOYMENT_FAILED" >> playbook_output.log
            exit 1
          }
      - name: Upload Logs
        if: always()
        uses: actions/upload-artifact@v4
        with: { name: execution-logs, path: playbook_output.log }
EOF

    # --- WORKFLOW: AUTO MERGE ---
    cat <<'EOF' > .github/workflows/auto-merge.yml
name: Auto Merge and Close
on:
  pull_request: { types: [opened, ready_for_review] }
jobs:
  merge-and-close:
    runs-on: ubuntu-latest
    steps:
      - name: Wait for Verification
        run: gh pr checks "${{ github.event.pull_request.html_url }}" --required --watch
        env: { GH_TOKEN: ${{ secrets.GITHUB_TOKEN }} }
      - name: Merge
        env: { GH_TOKEN: ${{ secrets.GITHUB_TOKEN }} }
        run: |
          PR_URL="${{ github.event.pull_request.html_url }}"
          ISSUE_NUM=$(gh pr view "$PR_URL" --json body -q '.body' | grep -oEi '(closes|fixes) #[0-9]+' | grep -oE '[0-9]+' | head -n 1)
          gh pr merge --auto --merge "$PR_URL"
          [ -n "$ISSUE_NUM" ] && gh issue close "$ISSUE_NUM" --comment "Auto-closed via containerized validation loop."
EOF

    echo "[5/5] Setup Complete! Next steps:"
    echo "1. git add . && git commit -m 'chore: setup isolated agentic workflow' && git push"
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
        --body "### Mission: Initialize Cluster Upbringing (Containerized)
- Verify bootstrap.sh --container logic works on host.
- Confirm folder structure (src/, tests/, ISSUES/).
- Generate follow-up tasks in ISSUES/ for core services."
    echo "✅ Issue #1 created. Automation engine is live with CONTAINER ISOLATION."
}

# ==========================================
# UNINSTALL LOGIC
# ==========================================
uninstall_workflow() {
    echo "Cleaning up Agentic configs..."
    rm -f .github/workflows/create-issues-from-files.yml .github/workflows/jules-queue.yml .github/workflows/remote-verify.yml .github/workflows/auto-merge.yml .github/AGENTIC_README.md
    rm -rf .github/context/ ISSUES/
    gh label delete "jules" --yes || true
    gh label delete "auto-generated" --yes || true
    if [ "$PURGE_NOMAD" = true ] && [ -f "./bootstrap.sh" ]; then
        echo "Purging Nomad jobs..."
        ./bootstrap.sh --purge-jobs
    fi
    echo "✅ Agentic workflow removed."
}

# --- Router ---
if [ "$ACTION" == "setup" ]; then setup_workflow;
elif [ "$ACTION" == "ignite" ]; then ignite_workflow;
elif [ "$ACTION" == "uninstall" ]; then uninstall_workflow;
elif [ "$ACTION" == "status" ]; then check_status; fi
