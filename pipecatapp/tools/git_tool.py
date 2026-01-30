import subprocess
import os

class Git_Tool:
    """A tool for interacting with Git repositories.

    This class provides methods to execute Git commands from within the
    agent's environment.
    """
    def __init__(self, root_dir=None):
        """Initializes the Git_Tool.

        Args:
            root_dir (str, optional): The directory to restrict git operations to.
                                      If None, defaults to the current working directory.
        """
        self.description = "A tool for interacting with Git repositories."
        self.name = "git_tool"
        if root_dir:
            self.root_dir = os.path.abspath(root_dir)
        else:
            self.root_dir = os.path.abspath(os.getcwd())

    def _validate_path(self, path: str) -> str:
        """Ensures the path is within the root directory."""
        # Resolve absolute path
        if not os.path.isabs(path):
            full_path = os.path.abspath(os.path.join(os.getcwd(), path))
        else:
            full_path = os.path.abspath(path)

        # Security check: Ensure we don't break out of the allowed root
        try:
            common = os.path.commonpath([self.root_dir, full_path])
        except ValueError:
            common = ""

        if common != self.root_dir:
            raise ValueError(f"Access denied: {path} is outside the allowed root {self.root_dir}")

        return full_path

    def _run_git_command(self, command: list, working_dir: str) -> str:
        """A helper function to run a Git command.

        Args:
            command (list): The Git command to run as a list of strings.
            working_dir (str): The directory to run the command in.

        Returns:
            str: A string containing the output of the command, or an
                error message if the run fails.
        """
        try:
            working_dir = self._validate_path(working_dir)
        except ValueError as e:
            return str(e)

        if not os.path.isdir(working_dir):
            return f"Error: Working directory '{working_dir}' not found."

        try:
            process = subprocess.run(
                ["git"] + command,
                cwd=working_dir,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            if process.returncode == 0:
                return f"Command successful.\nOutput:\n{process.stdout}"
            else:
                return f"Command failed with return code {process.returncode}.\nSTDOUT:\n{process.stdout}\nSTDERR:\n{process.stderr}"

        except subprocess.TimeoutExpired as e:
            return f"Error: Git command timed out after 5 minutes.\nSTDOUT:\n{e.stdout}\nSTDERR:\n{e.stderr}"
        except Exception as e:
            return f"An unexpected error occurred while trying to run Git: {e}"

    def clone(self, repo_url: str, directory: str) -> str:
        """Clones a Git repository.

        Args:
            repo_url (str): The URL of the repository to clone.
            directory (str): The directory to clone the repository into.

        Returns:
            str: The output of the git clone command.
        """
        # Validate that the target directory (relative to CWD) is within root
        # Note: 'directory' here is the argument to git clone, which creates it.
        # git clone <url> <directory>
        # We run it in "." (CWD).
        # So we should validate that os.path.join(os.getcwd(), directory) is safe.

        try:
            # We don't check existence because clone creates it, but we check location.
            self._validate_path(directory)
        except ValueError as e:
            return str(e)

        # Security Fix: Prevent path traversal
        if ".." in directory or os.path.isabs(directory):
            return "Error: Invalid directory. Path traversal is not allowed. Please use a relative path."

        return self._run_git_command(["clone", repo_url, directory], ".")

    def pull(self, working_dir: str) -> str:
        """Pulls changes from a remote repository.

        Args:
            working_dir (str): The path to the local repository.

        Returns:
            str: The output of the git pull command.
        """
        return self._run_git_command(["pull"], working_dir)

    def push(self, working_dir: str) -> str:
        """Pushes changes to a remote repository.

        Args:
            working_dir (str): The path to the local repository.

        Returns:
            str: The output of the git push command.
        """
        return self._run_git_command(["push"], working_dir)

    def commit(self, working_dir: str, message: str) -> str:
        """Commits changes to the local repository.

        Args:
            working_dir (str): The path to the local repository.
            message (str): The commit message.

        Returns:
            str: The output of the git commit command.
        """
        return self._run_git_command(["commit", "-m", message], working_dir)

    def branch(self, working_dir: str, branch_name: str = None) -> str:
        """Creates or lists branches.

        Args:
            working_dir (str): The path to the local repository.
            branch_name (str, optional): The name of the branch to create.
                If not provided, lists existing branches.

        Returns:
            str: The output of the git branch command.
        """
        command = ["branch"]
        if branch_name:
            command.append(branch_name)
        return self._run_git_command(command, working_dir)

    def checkout(self, working_dir: str, branch_name: str) -> str:
        """Checks out a branch.

        Args:
            working_dir (str): The path to the local repository.
            branch_name (str): The name of the branch to check out.

        Returns:
            str: The output of the git checkout command.
        """
        return self._run_git_command(["checkout", branch_name], working_dir)

    def status(self, working_dir: str) -> str:
        """Gets the status of the local repository.

        Args:
            working_dir (str): The path to the local repository.

        Returns:
            str: The output of the git status command.
        """
        return self._run_git_command(["status"], working_dir)

    def diff(self, working_dir: str, commit1: str = None, commit2: str = None) -> str:
        """Shows the differences between commits, branches, or the working directory.

        Args:
            working_dir (str): The path to the local repository.
            commit1 (str, optional): The first commit or branch to compare.
            commit2 (str, optional): The second commit or branch to compare.

        Returns:
            str: The output of the git diff command.
        """
        command = ["diff"]
        if commit1:
            command.append(commit1)
        if commit2:
            command.append(commit2)
        return self._run_git_command(command, working_dir)

    def merge(self, working_dir: str, branch: str) -> str:
        """Merges a branch into the current branch.

        Args:
            working_dir (str): The path to the local repository.
            branch (str): The name of the branch to merge.

        Returns:
            str: The output of the git merge command.
        """
        return self._run_git_command(["merge", branch], working_dir)

    def ls_files(self, working_dir: str) -> str:
        """Lists files in the work tree.

        Args:
            working_dir (str): The path to the local repository.

        Returns:
            str: The output of the git ls-files command.
        """
        return self._run_git_command(["ls-files"], working_dir)
