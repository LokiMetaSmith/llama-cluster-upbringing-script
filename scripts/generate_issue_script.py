import re

def parse_todo_file(filepath="TODO.md"):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    tasks = []
    current_task = None
    for line in lines:
        # Check for a new incomplete task
        match = re.match(r'^\s*-\s*\[\s\]\s*(.*)', line)
        if match:
            # If there was a previous task, save it
            if current_task:
                tasks.append(current_task)

            title = match.group(1).strip().replace('**', '')
            current_task = {"title": title, "body": ""}
        # If we are inside a task, collect the body
        elif current_task and line.strip().startswith('- '):
             # Only append if it's a sub-bullet, not another main task
            if not re.match(r'^\s*-\s*\[[x\s]\]\s*(.*)', line):
                current_task["body"] += line.strip().lstrip('- ') + "\\n"

    # Add the last task if it exists
    if current_task:
        tasks.append(current_task)

    return tasks

def create_issue_script(tasks, script_path="create_todo_issues.sh"):
    with open(script_path, 'w') as f:
        f.write("#!/bin/bash\n\n")
        f.write("echo \"This script will create GitHub issues for all incomplete tasks in TODO.md\"\n")
        f.write("echo \"Please ensure you have the 'gh' CLI tool installed and configured.\"\n\n")

        for task in tasks:
            title = task['title'].replace('"', '\\"') # Escape quotes for shell
            body = task['body'].replace('"', '\\"')

            # Remove any trailing newlines from the body
            body = body.strip()

            if body:
                f.write(f'gh issue create --title "{title}" --body "{body}"\n')
            else:
                f.write(f'gh issue create --title "{title}"\n')

if __name__ == "__main__":
    all_tasks = parse_todo_file()
    create_issue_script(all_tasks)
    print(f"Generated create_todo_issues.sh with {len(all_tasks)} issues.")
