import os
import requests
import urllib.parse
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
                                "Env": {
                                    "CONFIG_JSON": json.dumps(config)
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

            return {
                "stage": stage,
                "job_id": job_id,
                "status": "success" if success else "failed",
                "message": f"Stage {stage} {'completed successfully' if success else 'failed or timed out'}."
            }
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
