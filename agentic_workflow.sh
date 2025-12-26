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
      - name: Checkout repo
        uses: actions/checkout@v4
      - name: Create issues from ISSUES dir
        env: { GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }} }
        shell: bash
        run: |
          # 0. ENSURE LABEL EXISTS
          gh label create "auto-generated" \
            --repo "$GITHUB_REPOSITORY" \
            --description "Issues created from files" \
            --color "ededed" || true

          # 1. BATCH FETCH EXISTING ISSUES
          echo "Fetching existing issues..."
          gh issue list \
            --repo "$GITHUB_REPOSITORY" \
            --label "auto-generated" \
            --state all \
            --limit 1000 \
            --json title \
            --jq '.[].title' > existing_titles.txt

          # 2. GENERATE SORTED FILE LIST (safe guard)
          echo "Identifying and sorting files..."
          files=$(find ISSUES issues -maxdepth 1 -name "*.md" -type f 2>/dev/null | sort -V || true)
          if [ -z "$files" ]; then
              echo "No markdown files found in ISSUES/ or issues/. Exiting gracefully."
              exit 0
          fi
          printf "%s\n" "$files" > sorted_files.txt

          # 3. LOOP THROUGH SORTED LIST
          while IFS= read -r file; do
              filename=$(basename "$file")
              expected_title="Issue for $filename"
              if grep -Fxq "$expected_title" existing_titles.txt; then
                  echo "Skipping: $filename (exists)"
                  continue
              fi

              echo "Creating issue for: $filename"
              body_file=$(mktemp)
              {
                  echo "This issue was automatically created for file: \`$file\`."
                  echo ""
                  echo "### Content"
                  echo "\`\`\`"
                  cat "$file"
                  echo ""
                  echo "\`\`\`"
                  echo ""
                  echo "---"
                  echo "### Directive: Recursive Task Generation"
                  echo ""
                  echo "**Context:** Every task MUST be analyzed for:"
                  echo "- Dependencies (code, infra, configs)"
                  echo "- Refactoring (duplication, naming, structure)"
                  echo "- Extensions (tests, docs, automation)."
                  echo ""
                  echo "**Requirement:** Do not inline future work in comments. At least ONE follow-up issue MUST be created for every task, we can always improve something"
                  echo ""
                  echo "**Output Specification:**"
                  echo "1. **Action:** Create one or more markdown files."
                  echo "2. **Path:** \`ISSUES/<kebab-case-description>.md\`"
                  echo "3. **Content:** Detailed technical scope and acceptance criteria."
              } > "$body_file"

              gh issue create \
                --title "$expected_title" \
                --body-file "$body_file" \
                --label "auto-generated" \
                --repo "$GITHUB_REPOSITORY"
              sleep 2
          done < sorted_files.txt
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
    permissions:
      issues: write
    env: { GH_TOKEN: ${{ secrets.IMPERSONATION_PAT }}, MAX_RUNS: ${{ vars.JULES_MAX_DAILY_RUNS || '10' }} }
    steps:
      - name: Manage Jules Label
        run: |
          # 1. RATE LIMIT CHECK
          SINCE=$(date -u -d '24 hours ago' '+%Y-%m-%dT%H:%M:%SZ')
          RECENT_COUNT=$(gh search issues --repo "${{ github.repository }}" --label "jules" --updated ">$SINCE" --json number --jq 'length')
          RECENT_COUNT=${RECENT_COUNT:-0}
          echo "[INFO] Activity Monitor: $RECENT_COUNT issues processed in last 24h."

          if [ "$RECENT_COUNT" -ge "$MAX_RUNS" ]; then
             echo "[LIMIT] Daily limit of $MAX_RUNS reached. Sleeping until activity cools down."
             exit 0
          fi

          # 2. CHECK ACTIVE ISSUE & STALL DETECTION
          active=$(gh issue list --repo "${{ github.repository }}" --label "jules" --state open --json number,updatedAt --jq '.[0]')

          if [ -n "$active" ]; then
              issue_num=$(echo "$active" | jq '.number')
              updated_at=$(echo "$active" | jq -r '.updatedAt')
              echo "[INFO] Issue #$issue_num is currently active."

              # Stall Detection (2 hours)
              STALL_THRESHOLD=7200
              current_time=$(date +%s)
              last_update=$(date -d "$updated_at" +%s)
              diff=$((current_time - last_update))

              if [ "$diff" -gt "$STALL_THRESHOLD" ]; then
                  echo "[WARNING] Issue #$issue_num has been stuck for $diff seconds."
                  gh issue comment "$issue_num" --repo "${{ github.repository }}" \
                    --body "[SYSTEM ALERT] This issue has held the 'jules' label for over 2 hours without closing. The automation pipeline may be stuck. Please investigate." || true
              fi
              echo "[INFO] Waiting for issue #$issue_num to be processed. Done."
              exit 0
          fi

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
          next=$(gh issue list --repo "${{ github.repository }}" --state open --json number --jq 'min_by(.number).number')
          if [ -n "$next" ]; then
              echo "[ACTION] Promoting issue #$next to jules."
              gh issue edit "$next" --repo "${{ github.repository }}" --add-label "jules"
          else
              echo "[INFO] No open issues available to tag."
          fi
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
          echo "Triggered by CI success on branch $HEAD_BRANCH"
          PR_URL=$(gh pr list --repo "$REPO" --head "$HEAD_BRANCH" --state open --json url --jq '.[0].url')

          if [ -z "$PR_URL" ]; then
              echo "::notice ::No open PR found for branch $HEAD_BRANCH. Skipping auto-merge."
              exit 0
          fi

          echo "Found PR: $PR_URL"
          CHANGES=$(gh pr diff "$PR_URL" --name-only)

          if echo "$CHANGES" | grep -q "^\(ISSUES\|issues\)/"; then
              echo "[SUCCESS] Valid Issue Definition found."
              gh pr merge --merge "$PR_URL"

              PR_BODY=$(gh pr view "$PR_URL" --json body -q .body)
              ISSUE_NUMBER=$(echo "$PR_BODY" | grep -oEi '(close|closes|closed|fix|fixes|fixed|resolve|resolves|resolved) #[0-9]+' | grep -oE '[0-9]+' | head -n 1)

              if [ -n "$ISSUE_NUMBER" ]; then
                  echo "Closing linked issue #$ISSUE_NUMBER..."
                  gh issue close "$ISSUE_NUMBER" --repo "$REPO" --comment "Auto-closed via validation loop."
              fi
          else
              echo "[FAILURE] Violation: No changes detected in 'issues/' directory."
              gh pr comment "$PR_URL" --body "**[FAILURE] Entropy Detected**: This PR does not include a corresponding Issue Definition in \`issues/\`.
              **Action Required:**
              This project requires continuous forward motion. This PR cannot be merged until a **new** issue definition is created for the next logical step.
              **Agent Instructions:**
              1. Analyze the changes in this PR.
              2. Identify a logical follow-up task.
              3. **Create a new file** in \`ISSUES/\` with the format \`ISSUES/$(date --iso)-{topic}.md\`.
              4. The file must contain Title, Context, and Acceptance Criteria.
              **Auto-merge is blocked until this new file is detected.**"
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

    echo "[1/3] Generating Mission Brief..."
    mkdir -p .github/context
    cat <<'EOT' > .github/context/MISSION_BRIEF.md
### Mission Brief (User Requirements)
This is a placeholder mission brief.

CORE CONCEPT:
Describe the main idea of the project here in abstract terms.
Example: "Users interact with a system that provides value based on defined attributes."

TECH STACK:
- Placeholder frontend technology
- Placeholder backend/database technology
- Placeholder supporting services

PHASE 1 (MVP):
- Define the initial scope in abstract terms (e.g., "Start with a single region or dataset").
- Provide 2–3 sample placeholder items for demonstration only.
- Example Feature: "Filter by a generic attribute."

SCALING:
Architecture should be designed to support future expansion in a general sense.

---
### Agent Instructions
**Goal:** Initialize this repository and plan the next steps.
**Protocol:** Please strictly follow the steps defined in .github/context/SCAFFOLD_PROTOCOL.md.
EOT

    echo "[2/3] Generating Scaffolding Protocol..."
    cat <<'EOT' > .github/context/SCAFFOLD_PROTOCOL.md
# SCAFFOLDING PROTOCOL (AGENT INSTRUCTIONS)

## CONTEXT
You are the Lead Architect. You have been assigned the first issue in this repository.
Your goal is to initialize the repository structure based on the "Mission Brief".

## REQUIRED DELIVERABLES (The Definition of Done)
1. **The Foundation (Files)**
   - Create a .gitignore specific to the tech stack defined in the issue.
   - Create a README.md with the project name and "How to Run" instructions.
   - Create the physical directory structure (e.g., src/, tests/).

2. **The Standards (Linting & Style)**
   - CRITICAL: Create a .editorconfig to enforce line endings and indentation.
   - Set up the linter/formatter config (e.g., .eslintrc, rustfmt.toml, .prettierrc).

3. **The Governance (Memory)**
   - Create a file named .github/AI_CONTEXT.md.
   - In this file, summarize the decisions you made. Future Agents will read this.

## PROPAGATION (The Perpetual Engine)
You are responsible for keeping this project alive.

1. **Analyze:** Look at the scaffold you just built. What is missing?
2. **Create Task Files:**
   - Create a directory named `ISSUES` if it does not exist.
   - Create 2-3 new markdown files inside `ISSUES/` for the next logical steps.
   - **Ordering:** If the execution order of these new tasks is important, they MUST be ordered **relative to each other only**. Use numeric filename prefixes to enforce this sequence (e.g., `01-setup-database.md`, `02-run-migrations.md`).
   - **Format:** Each file MUST start with YAML frontmatter containing a `status: open` and `label: jules` field.
   - **Content:** Describe the task requirements in the file body.
EOT

    echo "[3/3] Creating First Issue..."
    gh issue create \
        --title "Scaffold: Initialize $REPO_NAME" \
        --label "jules" \
        --body-file .github/context/MISSION_BRIEF.md
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
