import sqlite3
import pickle
import os
import argparse
import sys

DB_PATH = os.path.expanduser("~/.config/pipecat/durable_execution.db")

def find_stalled_tasks(db_path):
    """Finds tasks that ended in a PENDING state or stopped mid-execution."""
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return []

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get the latest step sequence for each flowId
    cursor.execute("""
        SELECT e1.flowId, e1.step_sequence, e1.status
        FROM execution_log e1
        INNER JOIN (
            SELECT flowId, MAX(step_sequence) as max_seq
            FROM execution_log
            GROUP BY flowId
        ) e2 ON e1.flowId = e2.flowId AND e1.step_sequence = e2.max_seq
    """)

    tasks = []
    for row in cursor.fetchall():
        flow_id, max_seq, status = row
        # Consider tasks with PENDING status as stalled
        if status == "PENDING":
            tasks.append(flow_id)

    conn.close()
    return tasks

def extract_partial_work(db_path, task_id):
    """Extracts internal context and results from completed steps of a task."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT step_sequence, step_name, return_value, internal_context
        FROM execution_log
        WHERE flowId = ? AND status = 'COMPLETE'
        ORDER BY step_sequence ASC
    """, (task_id,))

    completed_steps = []
    last_context = None

    for row in cursor.fetchall():
        seq, name, ret_blob, ctx_blob = row

        try:
            ret_val = pickle.loads(ret_blob) if ret_blob else None
        except Exception:
            ret_val = "<unpickleable>"

        try:
            ctx = pickle.loads(ctx_blob) if ctx_blob else None
            if ctx:
                last_context = ctx
        except Exception:
            ctx = None

        completed_steps.append({
            "sequence": seq,
            "name": name,
            "return_value": ret_val
        })

    conn.close()
    return completed_steps, last_context

def synthesize_summary(completed_steps, last_context):
    """Synthesizes a simple summary of the extracted progress."""
    if not completed_steps:
        return "No completed steps found."

    summary = "### Executed Steps\n"
    for step in completed_steps:
        summary += f"- Step {step['sequence']} ({step['name']}): \n"
        ret = str(step['return_value'])
        # Truncate long return values
        if len(ret) > 200:
            ret = ret[:200] + "..."
        summary += f"  Result: {ret}\n"

    if last_context and "messages" in last_context:
        summary += "\n### Final Conversation Context\n"
        # Print the last few messages
        msgs = last_context["messages"][-3:] if len(last_context["messages"]) > 3 else last_context["messages"]
        for msg in msgs:
            summary += f"- {msg.get('role', 'unknown')}: "
            content = str(msg.get('content', ''))
            if len(content) > 150:
                content = content[:150] + "..."
            summary += f"{content}\n"

    return summary

def create_re_injection_prompt(original_goal, summary):
    """Generates the prompt to reinject the task."""
    prompt = f"""A previous attempt at this task stalled before completion.

Original Goal:
{original_goal}

Here is the data and context already gathered from the previous attempt:
{summary}

Your task is to continue from here and achieve the original goal. Do not repeat the completed steps if the results are already provided above. Focus on the remaining work."""
    return prompt

def main():
    parser = argparse.ArgumentParser(description="Extract and salvage partial work from stalled tasks.")
    parser.add_argument("--db", default=DB_PATH, help="Path to durable execution database")
    parser.add_argument("--task-id", help="Specific task ID to salvage. If omitted, lists stalled tasks.")
    parser.add_argument("--goal", help="The original goal of the task (used for the re-injection prompt).")

    args = parser.parse_args()

    if not args.task_id:
        stalled = find_stalled_tasks(args.db)
        if not stalled:
            print("No stalled tasks found.")
        else:
            print("Stalled Tasks (ended in PENDING):")
            for t in stalled:
                print(f"  - {t}")
            print("\nRun again with --task-id <id> and --goal <goal_text> to generate a salvage prompt.")
        sys.exit(0)

    steps, context = extract_partial_work(args.db, args.task_id)
    if not steps:
        print(f"No partial work found for task {args.task_id}.")
        sys.exit(1)

    print(f"Successfully extracted {len(steps)} completed steps for task {args.task_id}.")
    summary = synthesize_summary(steps, context)

    print("\n" + "="*50)
    print("SALVAGE SUMMARY:")
    print("="*50)
    print(summary)

    if args.goal:
        prompt = create_re_injection_prompt(args.goal, summary)
        print("\n" + "="*50)
        print("RE-INJECTION PROMPT:")
        print("="*50)
        print(prompt)

if __name__ == "__main__":
    main()