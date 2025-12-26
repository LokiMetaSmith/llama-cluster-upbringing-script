#!/bin/bash

# --- Help Menu ---
show_help() {
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  --setup      Install the Agentic Workflow (Jules) infrastructure."
    echo "  --uninstall  Remove all Agentic Workflow files and clean GitHub labels."
    echo "  --purge      (Used with --uninstall) Also purge all Nomad jobs using bootstrap.sh."
    echo "  -h, --help   Display this help message."
}

# --- Initialization ---
ACTION=""
PURGE_NOMAD=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --setup) ACTION="setup" ; shift ;;
        --uninstall) ACTION="uninstall" ; shift ;;
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
# SETUP LOGIC
# ==========================================
setup_workflow() {
    echo "[1/4] Creating directory structure..."
    mkdir -p .github/workflows
    mkdir -p .github/context
    mkdir -p ISSUES

    echo "[2/4] Writing GitHub Action workflows..."

    # --- 1. CREATE ISSUES FROM FILES ---
    cat <<'EOF' > .github/workflows/create-issues-from-files.yml
name: Create Issues from Files
on:
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
          files=$(find ISSUES issues -maxdepth 1 -name "*.md" -type f 2>/dev/null | sort -V || true)
          for file in $files; do
            filename=$(basename "$file")
            gh issue create --title "Issue for $filename" --body "Created from $file" --label "auto-generated" --repo "$GITHUB_REPOSITORY"
          done
EOF

    # --- 2. JULES QUEUE (LOG EVALUATOR) ---
    cat <<'EOF' > .github/workflows/jules-queue.yml
name: Jules Label Queue
on:
  issues: { types: [opened, labeled, closed] }
  workflow_run: { workflows: ["Auto Merge and Close"], types: [completed] }
jobs:
  enforce-jules:
    runs-on: ubuntu-latest
    env: { GH_TOKEN: ${{ secrets.IMPERSONATION_PAT }} }
    steps:
      - name: Evaluate Native Playbook Logs
        run: |
          RUN_ID=$(gh run list --workflow "Remote Verification" --limit 1 --json databaseId -q '.[0].databaseId')
          if [ -n "$RUN_ID" ]; then
            gh run download "$RUN_ID" --name execution-logs --dir ./remote_logs || true
            if [ -f "./remote_logs/playbook_output.log" ]; then
              if grep -Ei "failed=[1-9]|unreachable=[1-9]|DEPLOYMENT_FAILED" ./remote_logs/playbook_output.log > /dev/null; then
                ISSUE_NUM=$(gh issue list --label "jules" --state open --json number -q '.[0].number')
                gh issue comment "$ISSUE_NUM" --body "### ❌ Cluster Playbook Failed\n\`\`\`text\n$(tail -n 30 ./remote_logs/playbook_output.log)\n\`\`\`"
                exit 1
              fi
            fi
          fi
      - name: Promote Next
        run: |
          next=$(gh issue list --state open --json number --jq 'min_by(.number).number')
          if [ -n "$next" ]; then gh issue edit "$next" --add-label "jules"; fi
EOF

    # --- 3. REMOTE VERIFY (CALLS BOOTSTRAP.SH DIRECTLY) ---
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
      - name: Run Cluster Bootstrap
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

    # --- 4. AUTO MERGE ---
    cat <<'EOF' > .github/workflows/auto-merge.yml
name: Auto Merge and Close
on:
  pull_request: { types: [opened, ready_for_review] }
jobs:
  merge-and-close:
    runs-on: ubuntu-latest
    steps:
      - name: Wait for Verification
        env: { GH_TOKEN: ${{ secrets.GITHUB_TOKEN }} }
        run: gh pr checks "${{ github.event.pull_request.html_url }}" --required --watch
      - name: Merge
        env: { GH_TOKEN: ${{ secrets.GITHUB_TOKEN }} }
        run: gh pr merge --auto --merge "${{ github.event.pull_request.html_url }}"
EOF

    echo "[3/4] Creating protocol..."
    cat <<'EOF' > .github/context/SCAFFOLD_PROTOCOL.md
# Agent Protocol
1. Use ./bootstrap.sh --debug to verify all infra changes.
2. If playbook_output.log shows a failure, fix the playbook before proceeding.
3. Create new tasks in ISSUES/ with status: open and label: jules.
EOF

    echo "[4/4] Installation Complete!"
    echo "Next: Push these changes and set your IMPERSONATION_PAT secret in GitHub."
}

# ==========================================
# UNINSTALL LOGIC
# ==========================================
uninstall_workflow() {
    echo "[1/3] Removing Workflow and Context files..."
    rm -f .github/workflows/create-issues-from-files.yml
    rm -f .github/workflows/jules-queue.yml
    rm -f .github/workflows/remote-verify.yml
    rm -f .github/workflows/auto-merge.yml
    rm -rf .github/context/
    rm -rf ISSUES/

    echo "[2/3] Cleaning up GitHub labels..."
    if command -v gh &> /dev/null; then
        gh label delete "jules" --yes || true
        gh label delete "auto-generated" --yes || true
    else
        echo "⚠️  gh CLI not found; delete 'jules' label manually."
    fi

    if [ "$PURGE_NOMAD" = true ]; then
        echo "[3/3] Purging Nomad jobs via bootstrap.sh..."
        if [ -f "./bootstrap.sh" ]; then
            ./bootstrap.sh --purge-jobs
        else
            echo "❌ bootstrap.sh not found; could not purge jobs."
        fi
    fi

    echo "✅ Agentic workflow disabled."
}

# Execute based on flag
if [ "$ACTION" == "setup" ]; then
    setup_workflow
else
    uninstall_workflow
fi
