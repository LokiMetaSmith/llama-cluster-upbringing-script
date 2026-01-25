# Performance & I/O Optimization

This document tracks optimizations applied to the codebase to reduce syscall overhead and improve I/O performance, inspired by insights on [syscall overhead](https://modulovalue.com/blog/syscall-overhead-tar-gz-io-performance/).

## Syscall Reduction in ExperimentTool

**Problem:** The `ExperimentTool` creates a fresh sandbox for every agent evaluation. Previously, this used `shutil.copytree`, which performs thousands of `open`, `read`, `write`, `close` syscalls (one set per file) to copy the application code to a temporary directory.

**Solution:** We implemented a "Snapshot & Extract" strategy:
1.  A tar archive of the source directory is created once (excluding `.git`, `__pycache__`, etc.).
2.  For each sandbox, this tar archive is extracted using the system `tar` command.
3.  This replaces thousands of random read/write syscalls with a sequential read of the archive and optimized extraction, significantly speeding up sandbox creation.

## Git Integration in ProjectMapperTool

**Problem:** `ProjectMapperTool` used `os.walk` and Python-level filtering to scan the codebase. This is slow for large repositories and redundant when `git` already knows which files are tracked.

**Solution:** We updated `ProjectMapperTool` to use `git ls-files` when running inside a git repository. This offloads the file listing and ignore-pattern handling to `git`, which is highly optimized.

## Future Opportunities

-   **Batch I/O:** Look for other areas where many small files are processed and consider using `tar` or `sqlite` as a container.
-   **Logging:** Ensure logging doesn't open/close files excessively.
-   **Git Cat-File:** For tools reading many files, consider `git cat-file --batch` to read contents without opening individual file descriptors.
