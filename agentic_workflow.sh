#!/bin/bash

# --- Help Menu ---
show_help() {
    echo "Agentic Workflow Manager for Llama-Cluster"
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  --setup      Install robust workflows, protocol, and README."
    echo "  --uninstall  Remove workflow files and clean GitHub labels."
    echo "  --status     Check Jules queue state and stall detection."
    echo "  --purge      (With --uninstall) Purge Nomad jobs via bootstrap.sh."
}

# --- Initialization ---
ACTION=""
PURGE_NOMAD=false
while [[ $# -gt 0 ]]; do
    case "$1" in
        --setup) ACTION="setup" ; shift ;;
        --uninstall) ACTION="uninstall" ; shift ;;
        --status) ACTION="status" ; shift ;;
        --purge) PURGE_NOMAD=true ; shift ;;
        *) show_help ; exit 1 ;;
    esac
done

if [ -z "$ACTION" ]; then show_help ; exit 1 ; fi

# ==========================================
# STATUS LOGIC
# ==========================================
check_status() {
    echo "--- Agentic Workflow Status ---"
    if ! command -v gh &> /dev/null; then echo "❌ gh CLI not found" ; return 1 ; fi

    ACTIVE_ISSUE=$(gh issue list --label "jules" --state open --json number,title,updatedAt --jq '.[0]')
    
    if [ -n "$ACTIVE_ISSUE" ] && [ "$ACTIVE_ISSUE" != "null" ]; then
        ISSUE_NUM=$(echo "$ACTIVE_ISSUE" | jq -r '.number')
        UPDATED_AT=$(echo "$ACTIVE_ISSUE" | jq -r '.updatedAt')
        
        CURRENT_TS=$(date +%s)
        LAST_TS=$(date -d "$UPDATED_AT" +%s 2>/dev/null || date -j -f "%Y-%m-%dT%H:%M:%SZ" "$UPDATED_AT" +%s)
        DIFF=$((CURRENT_TS - LAST_TS))
        
        echo "📍 Active Task: Issue #$ISSUE_NUM"
        echo "🕒 Last Activity: $((DIFF / 3600))h $(((DIFF % 3600) / 60))m ago"
        [ "$DIFF" -gt 7200 ] && echo "⚠️  STATUS: STALLED (Threshold >2h)" || echo "✅ STATUS: ACTIVE"
    else
        echo "📭 STATUS: IDLE"
    fi
    echo "📊 Queue Depth: $(gh issue list --state open --limit 100 --json number --jq 'length') issues"
}

# ==========================================
# SETUP LOGIC
# ==========================================
setup_workflow() {
    echo "[1/5] Creating directory structure..."
    mkdir -p .github/workflows .github/context ISSUES src tests

    echo "[2/5] Generating Agentic README & Validation Loop Guide..."
    cat <<'EOF' > .github/AGENTIC_README.md
# Agentic Validation Loop Architecture

This repository utilizes a "Validation Loop" to bridge the AI agent with your local workstation hardware.

## 1. The Architecture
- **Step A:** Jules implements code changes and pushes them.
- **Step B:** A Verification Workflow triggers on your **Self-Hosted Runner**.
- **Step C:** The workstation executes `./bootstrap.sh --debug`, capturing logs to `playbook_output.log`.
- **Step D:** Jules evaluates the logs. If errors exist (e.g., Ansible `failed=1`), it iterates; otherwise, it merges.

## 2. Requirements
- **GitHub Self-Hosted Runner:** Must be installed on the workstation.
- **Secret `IMPERSONATION_PAT`:** Classic PAT with `repo` and `workflow` scopes.
- **Variable `JULES_MAX_DAILY_RUNS`:** Default is 10 to prevent infinite loops.

## 3. The Workflows
- `remote-verify.yml`: Executes the actual cluster upbringing on your hardware.
- `jules-queue.yml`: Orchestrates task priority and inspects remote logs.
- `auto-merge.yml`: Finalizes the PR once the validation loop passes.
EOF

    echo "[3/5] Writing robust workflow files..."

    # CREATE ISSUES (With Duplicate Check)
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
      - name: Process Files
        env: { GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }} }
        run: |
          gh label create "auto-generated" --repo "$GITHUB_REPOSITORY" --color "ededed" || true
          gh issue list --label "auto-generated" --state all --limit 1000 --json title --jq '.[].title' > existing_titles.txt
          files=$(find ISSUES issues -maxdepth 1 -name "*.md" -type f 2>/dev/null | sort -V || true)
          for file in $files; do
            expected_title="Issue for $(basename "$file")"
            if grep -Fxq "$expected_title" existing_titles.txt; then continue; fi
            body_file=$(mktemp)
            { echo "Automatically created for: \`$file\`"; echo "### Content"; echo '```'; cat "$file"; echo '```'; echo "---"; echo "### Directive: Recursive Task Generation"; echo "At least ONE follow-up issue MUST be created for every task."; } > "$body_file"
            gh issue create --title "$expected_title" --body-file "$body_file" --label "auto-generated"
          done
EOF

    # JULES QUEUE (Rate Limit + Log Inspector)
    cat <<'EOF' > .github/workflows/jules-queue.yml
name: Jules Label Queue
on:
  issues: { types: [opened, labeled, unlabeled, closed, reopened] }
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
          if [ "${RECENT:-0}" -ge "$MAX_RUNS" ]; then exit 0; fi
          active=$(gh issue list --label "jules" --state open --json number --jq '.[0]')
          if [ -n "$active" ]; then exit 0; fi

      - name: Evaluate Native Playbook Logs
        run: |
          RUN_ID=$(gh run list --workflow "Remote Verification" --limit 1 --json databaseId -q '.[0].databaseId')
          if [ -n "$RUN_ID" ]; then
            gh run download "$RUN_ID" --name execution-logs --dir ./remote_logs || true
            if [ -f "./remote_logs/playbook_output.log" ]; then
              if grep -Ei "failed=[1-9]|unreachable=[1-9]|DEPLOYMENT_FAILED" ./remote_logs/playbook_output.log > /dev/null; then
                ISSUE_NUM=$(gh issue list --label "jules" --state open --json number -q '.[0].number')
                gh issue comment "$ISSUE_NUM" --body "### ❌ Remote Run Failed\n\`\`\`text\n$(tail -n 30 ./remote_logs/playbook_output.log)\n\`\`\`"
                exit 1
              fi
            fi
          fi
      - name: Promote Next
        run: |
          next=$(gh issue list --state open --json number --jq 'min_by(.number).number')
          if [ -n "$next" ]; then gh issue edit "$next" --add-label "jules"; fi
EOF

    # REMOTE VERIFY (Direct Bootstrap Call)
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
      - name: Run Cluster Upbringing
        run: |
          chmod +x ./bootstrap.sh
          ./bootstrap.sh --debug --run-local --tags "app,verification" || {
            echo "DEPLOYMENT_FAILED" >> playbook_output.log
            exit 1
          }
      - name: Upload Logs
        if: always()
        uses: actions/upload-artifact@v4
        with: { name: execution-logs, path: playbook_output.log }
EOF

    # AUTO MERGE
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
          if [ -n "$ISSUE_NUM" ]; then gh issue close "$ISSUE_NUM" --comment "Auto-closed by validation loop."; fi
EOF

    echo "[4/5] Writing Protocol..."
    cat <<'EOF' > .github/context/SCAFFOLD_PROTOCOL.md
# Lead Architect Protocol
1. Every PR MUST include "Closes #X" in the body.
2. If remote logs show "failed=1", prioritize fixing the playbook.
3. Every task MUST generate a follow-up markdown file in ISSUES/.
EOF

    echo "[5/5] Setup Complete! Review .github/AGENTIC_README.md for next steps."
}

# ==========================================
# UNINSTALL LOGIC
# ==========================================
uninstall_workflow() {
    echo "Cleaning Agentic files..."
    rm -f .github/workflows/create-issues-from-files.yml .github/workflows/jules-queue.yml .github/workflows/remote-verify.yml .github/workflows/auto-merge.yml .github/AGENTIC_README.md
    rm -rf .github/context/ ISSUES/
    if command -v gh &> /dev/null; then
        gh label delete "jules" --yes || true
        gh label delete "auto-generated" --yes || true
    fi
    [ "$PURGE_NOMAD" = true ] && [ -f "./bootstrap.sh" ] && ./bootstrap.sh --purge-jobs
    echo "✅ Agentic workflow uninstalled."
}

if [ "$ACTION" == "setup" ]; then setup_workflow;
elif [ "$ACTION" == "uninstall" ]; then uninstall_workflow;
elif [ "$ACTION" == "status" ]; then check_status; fi
