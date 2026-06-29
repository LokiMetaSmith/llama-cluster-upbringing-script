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

    def _generate_mock_job_def(self, stage: str, job_id: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates a mock Nomad job definition for a given stage.
        """
        job = {
            "Job": {
                "ID": job_id,
                "Name": f"mtac-{stage}-{job_id.split(\"-\")[2][:8]}",
                "Type": "batch",
                "Datacenters": ["dc1"],
                "TaskGroups": [
                    {
                        "Name": "trainer",
                        "Tasks": [
                            {
                                "Name": f"{stage}-task",
                                "Driver": "raw_exec",
                                "Config": {
                                    "command": "/bin/sh",
                                    "args": [
                                        "-c",
                                        f"echo 'Starting mock {stage} with config: {json.dumps(config)}'; sleep 5; echo 'Finished mock {stage}'"
                                    ]
                                },
                                "Resources": {
                                    "CPU": 100,
                                    "MemoryMB": 64
                                }
                            }
                        ],
                        "RestartPolicy": {
                            "Attempts": 0,
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
        job_def = self._generate_mock_job_def(stage, job_id, config)

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
