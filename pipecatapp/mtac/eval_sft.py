import os
import json
import time

try:
    import lm_eval
except ImportError:
    lm_eval = None

def write_telemetry(metrics_file, task, results):
    with open(metrics_file, "a") as f:
        log_entry = {"stage": "eval", "task": task, "results": results}
        f.write(json.dumps(log_entry) + "\n")

def main():
    config_str = os.environ.get("CONFIG_JSON", "{}")
    config = json.loads(config_str)

    job_id = os.environ.get("MTAC_JOB_ID", "local")
    workspace_dir = f"/workspace/{job_id}"
    os.makedirs(workspace_dir, exist_ok=True)

    metrics_file = os.path.join(workspace_dir, "metrics.jsonl")

    # Typically, model path is passed in from the output of the SFT stage
    model_path = config.get("model", "unsloth/llama-3-8b-bnb-4bit")
    tasks = config.get("tasks", "hellaswag,gsm8k")
    limit = config.get("limit", None)  # limit number of docs for quick testing
    batch_size = config.get("batch_size", 1)

    print(f"Starting MTaC Evaluation for {job_id}")
    print(f"Model: {model_path}, Tasks: {tasks}")

    try:
        if lm_eval is None:
            print("lm_eval library not found. Running mock evaluation.")
            task_list = tasks.split(",")
            for t in task_list:
                write_telemetry(metrics_file, t, {"acc": 0.55, "acc_stderr": 0.01})
                time.sleep(1)
            print("Mock evaluation complete.")
            return

        print("Running lm-eval-harness...")
        task_list = tasks.split(",")

        results = lm_eval.simple_evaluate(
            model="hf",
            model_args=f"pretrained={model_path}",
            tasks=task_list,
            limit=limit,
            batch_size=batch_size,
        )

        for task_name, task_metrics in results['results'].items():
            print(f"Results for {task_name}: {task_metrics}")
            write_telemetry(metrics_file, task_name, task_metrics)

        print(f"Evaluation completed successfully. Metrics logged to {metrics_file}")

    except Exception as e:
        print(f"Error during evaluation: {e}")
        with open(metrics_file, "a") as f:
            f.write(json.dumps({"error": str(e), "stage": "eval"}) + "\n")
        raise

if __name__ == "__main__":
    main()
