#!/bin/bash

# --- Help Menu ---
show_help() {
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  --setup      Install the Agentic Workflow infrastructure (with Rate Limiting)."
    echo "  --uninstall  Remove all Agentic Workflow files and clean GitHub labels."
    echo "  --status     Check the state of the Jules queue and detect stalls."
    echo "  --purge      (With --uninstall) Purge Nomad jobs via cluster bootstrap.sh."
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
# STATUS LOGIC (Advanced Check)
# ==========================================
check_status() {
    echo "--- Agentic Workflow Status ---"
    ACTIVE_ISSUE=$(gh issue list --label "jules" --state open --json number,title,updatedAt --jq '.[0]')
    if [ -n "$ACTIVE_ISSUE" ] && [ "$ACTIVE_ISSUE" != "null" ]; then
        ISSUE_NUM=$(echo "$ACTIVE_ISSUE" | jq -r '.number')
        UPDATED_AT=$(echo "$ACTIVE_ISSUE" | jq -r '.updatedAt')
        CURRENT_TS=$(date +%s)
        LAST_TS=$(date -d "$UPDATED_AT" +%s 2>/dev/null || date -j -f "%Y-%m-%dT%H:%M:%SZ" "$UPDATED_AT" +%s)
        DIFF=$((CURRENT_TS - LAST_TS))
        echo "📍 Active Task: Issue #$ISSUE_NUM"
        [ "$DIFF" -gt 7200 ] && echo "⚠️  STATUS: STALLED (>2h)" || echo "✅ STATUS: ACTIVE"
    else
        echo "📭 STATUS: IDLE"
    fi
    echo "📊 Queue Depth: $(gh issue list --state open --limit 100 --json number --jq 'length') issues"
}

# ==========================================
# SETUP LOGIC (Merged Robust Version)
# ==========================================
setup_workflow() {
    echo "[1/4] Creating structure..."
    mkdir -p .github/workflows .github/context ISSUES src tests

    echo "[2/4] Writing robust workflows..."

    # 1. CREATE ISSUES (Includes Duplicate Check from your snippet)
    cat <<'EOF' > .github/workflows/create-issues-from-files.yml
name: Create Issues from Files
on:
  workflow_dispatch:
  push:
    paths: ["ISSUES/**", "issues/**"]
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
          gh label create "auto-generated" --repo "$GITHUB_REPOSITORY" --color "ededed" || true
          gh issue list --label "auto-generated" --state all --limit 1000 --json title --jq '.[].title' > existing_titles.txt
          files=$(find ISSUES issues -maxdepth 1 -name "*.md" -type f 2>/dev/null | sort -V || true)
          for file in $files; do
            expected_title="Issue for $(basename "$file")"
            grep -Fxq "$expected_title" existing_titles.txt && continue
            gh issue create --title "$expected_title" --body "Created from $file. At least ONE follow-up issue MUST be created." --label "auto-generated"
          done
EOF

    # 2. JULES QUEUE (Includes Rate Limiting + Native Log Check)
    cat <<'EOF' > .github/workflows/jules-queue.yml
name: Jules Label Queue
on:
  issues: { types: [opened, labeled, closed, reopened] }
  workflow_run: { workflows: ["Auto Merge and Close"], types: [completed] }
  schedule: [{cron: '0 * * * *'}]
jobs:
  enforce-jules:
    runs-on: ubuntu-latest
    env:
      GH_TOKEN: ${{ secrets.IMPERSONATION_PAT }}
      MAX_RUNS: ${{ vars.JULES_MAX_DAILY_RUNS || '10' }}
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
              if grep -Ei "failed=[1-9]|DEPLOYMENT_FAILED" ./remote_logs/playbook_output.log > /dev/null; then
                ISSUE_NUM=$(gh issue list --label "jules" --state open --json number -q '.[0].number')
                gh issue comment "$ISSUE_NUM" --body "### ❌ Cluster Playbook Failed\n\`\`\`text\n$(tail -n 25 ./remote_logs/playbook_output.log)\n\`\`\`"
                exit 1
              fi
            fi
          fi

      - name: Promote Next
        run: |
          next=$(gh issue list --state open --json number --jq 'min_by(.number).number')
          [ -n "$next" ] && gh issue edit "$next" --add-label "jules"
EOF

    # 3. REMOTE VERIFY (Calls cluster bootstrap.sh directly)
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
      - name: Upload Native Logs
        if: always()
        uses: actions/upload-artifact@v4
        with: { name: execution-logs, path: playbook_output.log }
EOF

    # 4. AUTO MERGE (Includes Issue Number Extraction logic)
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
          ISSUE_NUM=$(gh pr view "$PR_URL" --json body -q '.body' | grep -oEi 'closes #[0-9]+' | grep -oE '[0-9]+' | head -n 1)
          gh pr merge --auto --merge "$PR_URL"
          [ -n "$ISSUE_NUM" ] && gh issue close "$ISSUE_NUM" --comment "Auto-closed via PR"
EOF

    echo "[3/4] Writing Protocol..."
    cat <<'EOF' > .github/context/SCAFFOLD_PROTOCOL.md
# Lead Architect Protocol
1. Every PR must include "Closes #X" in the body.
2. Use ./bootstrap.sh --debug for verification.
3. Every task MUST generate a follow-up task in ISSUES/.
EOF

    echo "[4/4] Setup Complete!"
}

# ==========================================
# UNINSTALL LOGIC
# ==========================================
uninstall_workflow() {
    echo "Cleaning up..."
    rm -f .github/workflows/create-issues-from-files.yml .github/workflows/jules-queue.yml .github/workflows/remote-verify.yml .github/workflows/auto-merge.yml
    rm -rf .github/context/ ISSUES/
    gh label delete "jules" --yes || true
    gh label delete "auto-generated" --yes || true
    [ "$PURGE_NOMAD" = true ] && ./bootstrap.sh --purge-jobs
    echo "✅ Uninstalled."
}

if [ "$ACTION" == "setup" ]; then setup_workflow;
elif [ "$ACTION" == "uninstall" ]; then uninstall_workflow;
elif [ "$ACTION" == "status" ]; then check_status; fi
