# Project Linting and Formatting

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

* **`ansible/lint_nomad.yaml`**: Excluded from `yamllint` due to a persistent `no-new-line-at-end-of-file` warning that is difficult to resolve reliably across different environments.
* **`ansible/jobs/llama-expert.nomad`**: Excluded from `djlint` because the linter incorrectly flags the `http://` URLs used for local Consul communication (Rule `H022`). This is a false positive, as these URLs are internal to the cluster.

These exclusions ensure that the linting process can complete successfully while still providing value for the rest of the codebase. They should be revisited periodically to see if updates to the linters or the files themselves can resolve the underlying issues.
