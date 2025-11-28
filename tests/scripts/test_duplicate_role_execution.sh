#!/bin/bash
#
# Test to verify that the bootstrap_agent role is not run twice using static analysis.
#

# Move to the project root directory
cd "$(dirname "$0")/.."

echo "Starting test: test_duplicate_role_execution.sh"

# Run the playbook with --list-tasks to get a list of all tasks that would be executed.
# This is a static check and doesn't require sudo or running any actual commands.
# We pass a dummy 'target_user' because the playbook requires it.
playbook_tasks=$(ansible-playbook -i local_inventory.ini playbook.yaml --list-tasks -e "target_user=testuser")

# The task we are looking for is inside the 'bootstrap_agent' role.
# Ansible formats this as 'role_name : task_name'.
# We'll check for a task that is unique to the role.
TASK_NAME="bootstrap_agent : Print Nomad cluster members summary"

# Count the occurrences of the task name in the output.
# The 'grep -c' command will count the lines containing the task name.
OCCURRENCE_COUNT=$(echo "$playbook_tasks" | grep -c "Print Nomad cluster members summary")

# The expected count before the fix is 2.
EXPECTED_COUNT_BEFORE_FIX=2

echo "--------------------------------------------------"
echo "Checking for duplicate role execution using --list-tasks..."
echo "Searching for task signature: '${TASK_NAME}'"
echo "Found ${OCCURRENCE_COUNT} occurrences."
echo "--------------------------------------------------"

# For the purpose of this test, we are proving the bug exists.
# So we expect the count to be 2.
if [ "$OCCURRENCE_COUNT" -eq "$EXPECTED_COUNT_BEFORE_FIX" ]; then
    echo "✅ SUCCESS: Bug confirmed. The role would be executed twice."
    exit 0
else
    echo "❌ FAILURE: Test did not confirm the bug."
    echo "Expected ${EXPECTED_COUNT_BEFORE_FIX} occurrences, but found ${OCCURRENCE_COUNT}."
    echo "This might mean the bug is already fixed or the test logic is flawed."
    exit 1
fi