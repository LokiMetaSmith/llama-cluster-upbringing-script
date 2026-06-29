import os
import requests

import json
import asyncio
import logging
import uuid
import time
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class MTACPipelineOrchestrator:
    """
    Model Training as Code Pipeline Orchestrator.
    Handles generating and dispatching Nomad jobs for model training stages.
    """
    def __init__(self):
        cluster_ip = os.getenv("CLUSTER_IP", "127.0.0.1")
        self.nomad_addr = os.getenv("NOMAD_ADDR", f"http://{cluster_ip}:4646")

    def _generate_job_def(self, stage: str, job_id: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates a Nomad job definition for a given stage, supporting both mock and real ML container backends.
        """
        backend = config.get("backend", "mock").lower()
        shared_mount_point = "/opt/nomad/data/mtac"

        if backend == "mock":
            driver = "docker"
            driver_config = {
                "image": "alpine:latest",
                "command": "/bin/sh",
                "args": [
                    "-c",
                    f"echo \"Starting mock {stage} with config:\"; printenv CONFIG_JSON; sleep 5; echo \"Finished mock {stage}\""
                ]
            }
        else:
            driver = "docker"
            # Default images for the backends, can be overridden by config
            image = config.get("image")
            if not image:
                if backend == "unsloth":
                    image = "unsloth/unsloth:latest"
                elif backend == "torchtune":
                    image = "pytorch/torchtune:latest"
                else:
                    # Fallback generic python ML container
                    image = "pytorch/pytorch:latest"

            # Inject script template if backend supports it
            templates = []
            if backend == "unsloth" and stage == "sft":
                templates.append({
                    "DestPath": "local/train.py",
                    "EmbeddedTmpl": "import os\nimport json\nimport torch\nfrom datasets import load_dataset\ntry:\n    from unsloth import FastLanguageModel\n    from trl import SFTTrainer\nexcept ImportError:\n    # Handle mock environment where unsloth is missing\n    FastLanguageModel = None\n    SFTTrainer = None\nfrom transformers import TrainingArguments, TrainerCallback\n\nclass TelemetryCallback(TrainerCallback):\n    def __init__(self, log_file):\n        self.log_file = log_file\n\n    def on_log(self, args, state, control, logs=None, **kwargs):\n        if logs is not None:\n            with open(self.log_file, \"a\") as f:\n                log_entry = {\"step\": state.global_step}\n                log_entry.update(logs)\n                f.write(json.dumps(log_entry) + \"\\n\")\n\ndef main():\n    # Read config from environment variable\n    config_str = os.environ.get(\"CONFIG_JSON\", \"{}\")\n    config = json.loads(config_str)\n    \n    job_id = os.environ.get(\"MTAC_JOB_ID\", \"local\")\n    workspace_dir = f\"/workspace/{job_id}\"\n    os.makedirs(workspace_dir, exist_ok=True)\n    \n    metrics_file = os.path.join(workspace_dir, \"metrics.jsonl\")\n    \n    model_name = config.get(\"model\", \"unsloth/llama-3-8b-bnb-4bit\")\n    dataset_name = config.get(\"dataset\", \"yahma/alpaca-cleaned\")\n    max_steps = config.get(\"max_steps\", 60)\n    \n    print(f\"Starting MTaC SFT Training for {job_id}\")\n    print(f\"Model: {model_name}, Dataset: {dataset_name}, Steps: {max_steps}\")\n    \n    try:\n        if FastLanguageModel is None:\n            print(\"Unsloth library not found. Running mock loop.\")\n            for i in range(max_steps):\n                with open(metrics_file, \"a\") as f:\n                    f.write(json.dumps({\"step\": i, \"loss\": 2.0 / (i + 1)}) + \"\\n\")\n            print(\"Mock training complete.\")\n            return\n\n        model, tokenizer = FastLanguageModel.from_pretrained(\n            model_name=model_name,\n            max_seq_length=2048,\n            dtype=None,\n            load_in_4bit=True,\n        )\n        \n        model = FastLanguageModel.get_peft_model(\n            model,\n            r=16,\n            target_modules=[\"q_proj\", \"k_proj\", \"v_proj\", \"o_proj\", \"gate_proj\", \"up_proj\", \"down_proj\"],\n            lora_alpha=16,\n            lora_dropout=0,\n            bias=\"none\",\n            use_gradient_checkpointing=True,\n            random_state=3407,\n            use_rslora=False,\n            loftq_config=None,\n        )\n        \n        # Note: In production you would format the text column appropriately.\n        dataset = load_dataset(dataset_name, split=\"train[:1000]\") # small subset for testing\n        \n        trainer = SFTTrainer(\n            model=model,\n            tokenizer=tokenizer,\n            train_dataset=dataset,\n            dataset_text_field=\"text\",\n            max_seq_length=2048,\n            dataset_num_proc=2,\n            args=TrainingArguments(\n                per_device_train_batch_size=2,\n                gradient_accumulation_steps=4,\n                warmup_steps=5,\n                max_steps=max_steps,\n                learning_rate=2e-4,\n                fp16=not torch.cuda.is_bf16_supported(),\n                bf16=torch.cuda.is_bf16_supported(),\n                logging_steps=1,\n                optim=\"adamw_8bit\",\n                weight_decay=0.01,\n                lr_scheduler_type=\"linear\",\n                seed=3407,\n                output_dir=os.path.join(workspace_dir, \"outputs\"),\n            ),\n            callbacks=[TelemetryCallback(metrics_file)]\n        )\n        \n        trainer_stats = trainer.train()\n        \n        print(f\"Training completed successfully. Metrics logged to {metrics_file}\")\n        \n    except Exception as e:\n        print(f\"Error during training: {e}\")\n        with open(metrics_file, \"a\") as f:\n            f.write(json.dumps({\"error\": str(e)}) + \"\\n\")\n        raise\n\nif __name__ == \"__main__\":\n    main()\n",
                    "Envvars": False
                })

                # Override command to run the injected script if none provided
                if "command" not in config:
                    config["command"] = "python3"
                if "args" not in config:
                    config["args"] = ["local/train.py"]

            driver_config = {
                "image": image,
                "command": config.get("command", "python3"),
                "args": config.get("args", ["-c", f"print('Running {stage} with {backend} backend')"]),
                "volumes": [
                    f"{shared_mount_point}:/workspace"
                ],
                "work_dir": "/workspace"
            }

            # Optional GPU support
            if config.get("use_gpu", False):
                # Request a generic GPU device mapping in Docker driver config
                # In modern Nomad/Docker, we map devices or use nvidia runtime.
                # Adding standard device mapping config to expose GPUs:
                driver_config["gpus"] = "all" # Note: requires nomad nvidia plugin or docker runtime config

        job = {
            "Job": {
                "ID": job_id,
                "Name": f"mtac-{stage}-{job_id.split('-')[2][:8]}",
                "Type": "batch",
                "Datacenters": ["dc1"],
                "TaskGroups": [
                    {
                        "Name": "trainer",
                        "Tasks": [
                            {
                                "Name": f"{stage}-task",
                                "Driver": driver,
                                "Config": driver_config,
                                "Templates": templates if backend != "mock" else [],
                                "Env": {
                                    "CONFIG_JSON": json.dumps(config),
                                    "MTAC_JOB_ID": job_id
                                },
                                "Resources": {
                                    "CPU": config.get("cpu", 1000),
                                    "MemoryMB": config.get("memory_mb", 4096)
                                }
                            }
                        ],
                        "RestartPolicy": {
                            "Attempts": config.get("restart_attempts", 0),
                            "Mode": "fail"
                        }
                    }
                ]
            }
        }
        return job

    async def _dispatch_job(self, job_def: Dict[str, Any]) -> str:
        """
        Submits the job definition to Nomad and returns the eval ID.
        """
        url = f"{self.nomad_addr}/v1/jobs"
        try:
            # Run requests in thread to avoid blocking asyncio loop
            response = await asyncio.to_thread(requests.post, url, json=job_def, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            return data.get("EvalID", "")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise

    async def _wait_for_job_completion(self, job_id: str, timeout: int = 300) -> bool:
        """
        Polls the Nomad API until the batch job is dead/complete.
        Returns True if successful, False if failed or timeout.
        """
        url = f"{self.nomad_addr}/v1/job/{job_id}/allocations"
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                response = await asyncio.to_thread(requests.get, url, timeout=5.0)
                if response.status_code == 200:
                    allocs = response.json()
                    if not allocs:
                        await asyncio.sleep(2)
                        continue

                    # Check the latest allocation
                    alloc = allocs[0]
                    client_status = alloc.get("ClientStatus")
                    if client_status in ["complete", "failed", "lost"]:
                        logger.info(f"Job {job_id} reached terminal state: {client_status}")
                        return client_status == "complete"
            except Exception as e:
                logger.warning(f"Error polling Nomad API for job {job_id}: {e}")

            await asyncio.sleep(2)

        logger.error(f"Timeout waiting for job {job_id} to complete")
        return False

    async def run_stage(self, stage: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs a specific training pipeline stage.
        """
        job_id = f"mtac-{stage}-{str(uuid.uuid4())}"
        job_def = self._generate_job_def(stage, job_id, config)

        logger.info(f"Dispatching MTaC stage: {stage} with Job ID: {job_id}")

        try:
            await self._dispatch_job(job_def)
            success = await self._wait_for_job_completion(job_id)

            result = {
                "stage": stage,
                "job_id": job_id,
                "status": "success" if success else "failed",
                "message": f"Stage {stage} {'completed successfully' if success else 'failed or timed out'}."
            }

            # Read telemetry from shared workspace
            metrics_file = f"/opt/nomad/data/mtac/{job_id}/metrics.jsonl"
            if os.path.exists(metrics_file):
                telemetry = []
                try:
                    with open(metrics_file, "r") as f:
                        for line in f:
                            if line.strip():
                                telemetry.append(json.loads(line))
                    result["telemetry"] = telemetry
                except Exception as parse_e:
                    logger.warning(f"Failed to parse telemetry file {metrics_file}: {parse_e}")

            return result

        except Exception as e:
            logger.error(f"Failed to dispatch or monitor job {job_id}: {e}")
            return {
                "stage": stage,
                "job_id": job_id,
                "status": "error",
                "message": str(e)
            }

    async def run_full_pipeline(self, pipeline_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orchestrates an end-to-end pipeline (SFT -> RL -> Eval).
        """
        results = {}

        # SFT Stage
        sft_config = pipeline_config.get("sft", {})
        sft_result = await self.run_stage("sft", sft_config)
        results["sft"] = sft_result
        if sft_result["status"] != "success":
            return {"status": "failed", "stage_results": results}

        # RL Stage
        rl_config = pipeline_config.get("rl", {})
        rl_result = await self.run_stage("rl", rl_config)
        results["rl"] = rl_result
        if rl_result["status"] != "success":
            return {"status": "failed", "stage_results": results}

        # Eval Stage
        eval_config = pipeline_config.get("eval", {})
        eval_result = await self.run_stage("eval", eval_config)
        results["eval"] = eval_result

        overall_status = "success" if eval_result["status"] == "success" else "failed"
        return {"status": overall_status, "stage_results": results}
