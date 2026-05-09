# Dirac Integration Plan & TODO List

This document outlines the step-by-step plan to implement the "Hybrid Approach" for integrating Dirac's capabilities into our cluster.

## Phase 1: CLI Integration (Immediate Value)

The goal of Phase 1 is to wrap the official `dirac-cli` in a Python tool so our main agent can delegate tasks to it.

### Step 1: Ansible Environment Setup
We need to ensure Node.js and the `dirac-cli` are installed on the worker nodes where the tool will execute.
- [x] **Create/Update Ansible Tasks:** Modify `ansible/roles/pipecatapp/tasks/main.yml` (or create a new `node` role) to ensure Node.js (via NVM or apt) is installed.
- [x] **Install Dirac:** Add an Ansible task to run `npm install -g dirac-cli`.
- [x] **API Keys:** Ensure the necessary environment variables (e.g., `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, or local base URLs) are passed securely via SOPS/Vault to the `dirac` execution environment in Nomad.

### Step 2: Develop `DiracTool`
- [x] **Create Tool File:** Create `pipecatapp/tools/dirac_tool.py`.
- [x] **Define Schema:** Implement the `Tool` base class with arguments like `prompt` (the coding task) and optionally `mode` (e.g., `-y` for yolo auto-approve mode).
- [x] **Subprocess Execution:** Use `subprocess.Popen` or `asyncio.create_subprocess_shell` to execute `dirac -y "<prompt>"`.
- [x] **Stream Output:** Capture and stream the stdout/stderr of Dirac back to the main agent\'s context or UI so the user can monitor progress.
- [x] **Handle Exit Codes:** Parse the exit code to determine if the task was successful or if the agent needs to retry/intervene.

### Step 3: Register Tool & Prompting
- [x] **Register Tool:** Add `dirac_tool` to the `TOOL_REGISTRY` in `pipecatapp/agent_factory.py`.
- [x] **Update Router Prompt:** Update `ansible/roles/pipecatapp/files/prompts/router.txt` (or the specific coding expert\'s prompt) to instruct the agent on *when* to use `dirac_tool` vs the legacy `file_editor` (e.g., "For complex multi-file refactors, use dirac_tool...").

### Step 4: Testing & Verification
- [x] Write unit tests for `dirac_tool.py` mocking the subprocess call.
- [x] Run an integration test on the cluster: Ask the agent to "Use dirac to refactor the memory.py file". Verify Dirac runs, edits the file, and exits successfully.

---

## Phase 2: Native Inspiration (Long-term Resilience)

The goal of Phase 2 is to build Dirac's token-saving techniques natively into our Python `file_editor` tool, eventually removing the Node.js dependency.

### Step 1: Hash-Anchored Edits
- [x] **Analyze Dirac's Hash Logic:** Study how Dirac hashes lines (e.g., stripping whitespace, handling blank lines).
- [x] **Implement Python Hasher:** Create a utility function in `pipecatapp/utils/file_utils.py` that reads a file and generates a list of `(line_number, hash, content)`.
- [x] **Update `file_editor` schema:** Add a new command to the `file_editor` tool like `hash_replace`, which accepts a start_hash, end_hash, and the replacement text.
- [x] **Implement Replacement Logic:** Write the logic to find the exact line ranges based on the hashes and safely splice in the new text.

### Step 2: AST-Native Parsing (Python focus first)
- [ ] **Research Libraries:** Evaluate `ast` (built-in, read-only) vs `libcst` (Concrete Syntax Tree, better for modifying code while preserving comments/formatting).
- [ ] **Implement `ast_editor` Tool:** Create a new tool (or expand `file_editor`) with structural commands:
    - `extract_function(filepath, func_name, target_filepath)`
    - `rename_symbol(filepath, old_name, new_name)`
    - `add_import(filepath, import_statement)`
- [ ] **Test Robustness:** Ensure the AST editor gracefully handles syntax errors or malformed input without corrupting the file.

### Step 3: Multi-file Batching
- [ ] **Update Tool Schemas:** Modify the new `hash_replace` and `ast_editor` commands to accept lists of operations across multiple files in a single JSON payload.
- [ ] **Refactor Prompt:** Update the system prompt to explicitly teach the model how to batch these commands to save tokens.

### Step 4: Transition
- [ ] **Benchmarking:** Run our native tools through our internal TerminalBench suite. Compare token usage and success rate against the Node.js `dirac_tool`.
- [ ] **Deprecation:** Once parity is reached, remove `dirac_tool` from the active toolset and uninstall `dirac-cli` and Node.js from the worker node Ansible roles.