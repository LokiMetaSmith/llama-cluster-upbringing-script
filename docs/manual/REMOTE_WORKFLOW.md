# Improving Your Remote Workflow with Mosh and Tmux

Last updated: 2025-11-06

Managing a remote cluster involves spending a lot of time in a terminal. Mosh and tmux are two essential tools that make this experience faster, more reliable, and more efficient.

## Mosh: The Mobile Shell 🚀

Mosh is a replacement for SSH that is built for modern, unreliable network connections.

**What it does:** It establishes a connection over UDP and uses a state-synchronization protocol to keep your session alive, even if your internet connection drops or you change networks.

**Key Benefits:**

* **Connection Roaming:** You can close your laptop, move to a different Wi-Fi network, open it back up, and your session will be exactly where you left it. No more dropped SSH connections.
* **Instant Keystroke Response:** Mosh provides an instant local echo of your typing, making the terminal feel fast and responsive even on high-latency connections.

**How to Use It:**

Simply replace `ssh` with `mosh`:

```bash
mosh user@<your-server-ip>
```

## Tmux: The Terminal Multiplexer 🖥️

Tmux allows you to create persistent terminal sessions on your remote server that you can detach from and re-attach to later.

**What it does:** It runs a server process on your remote machine that hosts your terminal sessions. You can then connect to this server, create multiple windows and panes, and safely disconnect without terminating your running commands.

**Key Benefits:**

* **Persistent Sessions:** Start a long-running command (like building llama.cpp or downloading a model), detach from your tmux session, and close your local terminal. The command will continue to run on the server.
* **Multitasking:** Split your terminal into multiple panes to monitor logs in one while running commands in another, all within a single Mosh connection.

**How to Use It:**

* **Start a new session:**

    ```bash
    tmux new -s my-session-name
    ```

* **Detach from the session:** Press `Ctrl+b` then `d`.
* **List running sessions:**

    ```bash
    tmux ls
    ```

* **Re-attach to a session:**

    ```bash
    tmux attach -t my-session-name
    ```

## The Ultimate Combination: Mosh + Tmux ✨

Using Mosh and tmux together gives you the best of both worlds: a highly resilient connection to a persistent remote session.

### Your New Workflow

1. **Connect to your server with Mosh** for a stable, responsive shell:

    ```bash
    mosh user@<your-server-ip>
    ```

2. **Once connected, start or attach to a tmux session:**

    ```bash
    # To create a new session
    tmux new -s main

    # To attach to an existing session
    tmux a -t main
    ```

Now, you can work on your cluster with the confidence that neither a network drop nor a local crash will interrupt your long-running tasks.

## Beyond the Basics: Advanced Tools for Power Users 🚀

The following tools are not required, but they can significantly enhance your development experience, especially when working with code, files, and version control directly on the remote machine.

### Helix: A Modern, Post-Modern Text Editor

Helix is a modern text editor with a focus on simplicity and speed. It comes with language server support and other features built-in, requiring minimal configuration. It's a great alternative to Vim/Neovim if you find their plugin ecosystems complex.

**Key Benefits:**

* **Zero Configuration:** Comes with powerful features out-of-the-box, including tree-sitter for syntax highlighting and language server integration.
* **Modal Editing:** Uses a Kakoune-inspired modal editing model (select-then-act) which can be very efficient.
* **Fast and Lightweight:** Written in Rust, it's highly performant.

**Recommended `~/.config/helix/config.toml` setup:**

```toml
[editor]
line-number = "relative"
mouse = true
rulers = [120]
true-color = true
completion-replace = true
auto-save = true

[editor.file-picker]
hidden = false
```

### Tmux Popups: Integrating Tools Seamlessly

You can configure `tmux` to open common tools in convenient pop-up windows over your current session. This is great for quick file browsing or checking git status without leaving your editor.

Add the following to your `~/.tmux.conf` file:

```tmux
# Yazi, Lazygit, and Helix popups
# You may need to install yazi and lazygit first
# On Debian/Ubuntu:
# sudo add-apt-repository ppa:lazygit-team/release
# sudo apt-get update
# sudo apt-get install lazygit
# cargo install yazi-fm

set -g allow-passthrough on
set -ga update-environment TERM
set -ga update-environment TERM_PROGRAM

bind-key y display-popup -d '#{pane_current_path}' -x R -h 95% -w 95% -E 'tmux new-session yazi \; set status off'
bind-key g popup -E -w 95% -h 95%  -d '#{pane_current_path}' lazygit
bind-key e display-popup -w 95% -h 90% -E "tmux capture-pane -Jp -S- | hx -"
```

With this configuration (and after reloading your tmux config with `tmux source-file ~/.tmux.conf`), you can use the following shortcuts (assuming default `Ctrl+b` prefix):

* `prefix` + `y`: Opens the **Yazi** file manager in a popup.
* `prefix` + `g`: Opens **Lazygit** in a popup for easy git operations.
* `prefix` + `e`: Opens your terminal history in **Helix** for searching and copying.

### Yazi: A Blazing Fast Terminal File Manager

Yazi is a terminal file manager written in Rust. It's fast, has a clean interface, and integrates well with `tmux`.

**Key Benefits:**

* **Fast and Responsive:** Navigating large directories is snappy.
* **Visually Appealing:** Uses modern terminal features for a good-looking UI.
* **Great with Popups:** The `tmux` configuration above makes it a breeze to use.

### Lazygit: A TUI for Git

Lazygit provides a terminal-based user interface for git commands. It makes it easy to stage files, craft commits, and view your repository's history without having to remember all the git command-line flags.

**Key Benefits:**

* **Intuitive Interface:** Makes complex git operations much simpler.
* **Visual History:** Easily browse branches and commits.
* **Efficient:** Speed up your git workflow significantly.
