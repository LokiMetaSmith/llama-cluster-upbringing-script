# Project Linting and Formatting

Last updated: 2025-11-06

This document outlines the process for running linters to ensure code quality and consistency across the repository. The project uses a suite of linters for YAML, Markdown, Nomad (HCL), and Jinja2 files.

## 1. Installation

To run the linters, you must first install the necessary development dependencies.

### Python Dependencies

The Python-based linters (`yamllint`, `djlint`) are managed via `pip`. Install them by running the following command from the root of the repository:

```bash
pip install -r requirements-dev.txt
```

### Node.js Dependencies

The Markdown linter is managed via `npm`. Install it by running:

```bash
npm install
```

This will install the `markdownlint-cli` package listed in `devDependencies` in `package.json`.

## 2. Running the Linters

A unified script has been created to run all the linters with a single command.

From the root of the repository, run:

```bash
npm run lint
```

This command executes the `scripts/lint.sh` script, which will check all relevant files and report any errors.

## 3. Excluding Files (Whitelist)

Some files may have persistent, unresolvable linter errors due to tool limitations or specific project constraints. To prevent these from blocking the linting process, an exclusion system has been implemented.

### How it Works

The file `scripts/lint_exclude.txt` acts as a whitelist of files to be ignored by the linters. The main `scripts/lint.sh` script reads this file and dynamically generates the correct `--ignore` or `--exclude` flags for each linter.

To exclude a new file, simply add its full path (from the repository root) to a new line in `scripts/lint_exclude.txt`.

### Current Exclusions and Known Issues

The following files are currently excluded from linting:

- **`ansible/lint_nomad.yaml`**: Excluded from `yamllint` due to a persistent `no-new-line-at-end-of-file` warning that is difficult to resolve reliably across different environments.
- **`ansible/jobs/expert.nomad.j2`**: Excluded from `djlint` because the linter incorrectly flags the `http://` URLs used for local Consul communication (Rule `H022`). This is a false positive, as these URLs are internal to the cluster.

These exclusions ensure that the linting process can complete successfully while still providing value for the rest of the codebase. They should be revisited periodically to see if updates to the linters or the files themselves can resolve the underlying issues.

## 4. Ansible Playbook Change Detection

To ensure that changes to the Ansible playbooks are intentional and well-understood, the `ansible_diff.sh` script provides a way to compare playbook runs over time.

### Purpose

This script helps prevent unintended side effects by comparing the output of a "dry run" (`--check` mode) against a known-good "baseline" run. If the dry run output differs from the baseline, it means that applying the playbook will result in changes to the system.

### How it Works (Ansible Diff)

1. **Baseline Creation**: The first time you run the script, it executes the main playbook and saves its output to `ansible_run.baseline.log`. This file represents the expected state of the system.
2. **Comparison**: On subsequent runs, the script executes the playbook in `--check --diff` mode, which predicts changes without making them. It saves this output to a temporary log file.
3. **Difference Reporting**: The script then `diff`s the baseline log against the temporary check log. If differences are found, they are saved to `ansible_diff.log` for you to review.

### Usage

**Initial Run (Creating the Baseline):**

Before you can compare for changes, you must establish a baseline from a known-good system state.

1. First, ensure the system is configured correctly by running the main playbook.
2. Then, create the baseline with the `--update-baseline` flag:

```bash
./scripts/ansible_diff.sh --update-baseline
```

This will run the playbook in `--check --diff` mode and save its output to `ansible_run.baseline.log`.

**Checking for Changes:**

Once the baseline exists, run the script without any flags to compare the current playbook against the baseline:

```bash
./scripts/ansible_diff.sh
```

If changes are detected, review the `ansible_diff.log` file.

**Updating the Baseline:**

If you have made intentional changes to the playbooks and want to update the baseline to reflect the new expected state, run the same command as the initial setup:

```bash
./scripts/ansible_diff.sh --update-baseline
```

**Customizing the Run:**

You can override the default inventory and extra variables using command-line flags:

```bash
./scripts/ansible_diff.sh -i my_inventory.ini -e "target_user=other_user"
```

### Automated CI Check

For automated environments, the `ci_ansible_check.sh` script provides a wrapper around the `ansible_diff.sh` script that is suitable for use in CI/CD pipelines or as a pre-push git hook.

**Purpose:**

This script is designed to run non-interactively. It will:

- Exit with a status code of `0` if no changes are detected.
- Exit with a status code of `1` if changes are detected, printing the diff to standard output.

**How it Works (CI):**

The GitHub Actions workflow uses the `actions/cache` action to persist the `ansible_run.baseline.log` file across runs. The cache is keyed to the specific Git branch, so each pull request will have its own baseline.

- **First Run on a Branch:** When the workflow runs for the first time on a new branch, the cache will be empty. The script will detect that the baseline file is missing, create a new one, and exit successfully. The new baseline file is then saved to the cache for the next run.
- **Subsequent Runs:** On subsequent pushes to the same branch, the workflow will restore the baseline file from the cache. The script will then run the comparison against this restored baseline. If it finds a difference, it will print the diff and exit with an error, failing the CI job.

**Usage:**

This check runs automatically on every pull request. No manual intervention is needed.

**Updating the Baseline in a Pull Request:**

If a pull request introduces intentional changes to the Ansible playbooks, the `ansible-check` job will fail. To approve the changes and update the baseline for that branch, you must:

1. Navigate to the "Actions" tab in the GitHub repository.
2. Find the failed workflow run for your pull request.
3. Go to the "Cache" section and delete the cache entry corresponding to your branch (e.g., `ansible-baseline-refs/heads/your-branch-name`).
4. Re-run the failed job. It will now run on a clean cache, generate a new baseline, and pass successfully.
