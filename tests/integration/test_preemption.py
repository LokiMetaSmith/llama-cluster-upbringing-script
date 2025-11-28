import unittest
import os
import time
import nomad
import requests

class TestPreemption(unittest.TestCase):
    def setUp(self):
        self.nomad = nomad.Nomad(host=os.getenv("NOMAD_ADDR", "127.0.0.1"))
        self.world_model_url = os.getenv("WORLD_MODEL_URL", "http://localhost:8000")
        self.victim_job_name = "preemption-victim"
        self.victim_job = {
            "Job": {
                "ID": self.victim_job_name,
                "Name": self.victim_job_name,
                "Type": "service",
                "Datacenters": ["dc1"],
                "Priority": 50,
                "TaskGroups": [
                    {
                        "Name": "victim-group",
                        "Count": 1,
                        "Tasks": [
                            {
                                "Name": "victim-task",
                                "Driver": "raw_exec",
                                "Config": {
                                    "command": "sleep",
                                    "args": ["300"],
                                },
                                "Resources": {
                                    "CPU": 4000,
                                    "MemoryMB": 4096,
                                },
                            }
                        ],
                    }
                ],
            }
        }

    def tearDown(self):
        self.nomad.job.deregister_job(self.victim_job_name)

    def test_preemption(self):
        # 1. Register and run the victim job
        self.nomad.job.register_job(job=self.victim_job)
        time.sleep(5) # give time for the job to be placed

        # 2. Dispatch the high-priority job
        dispatch_response = requests.post(
            f"{self.world_model_url}/dispatch-job",
            json={
                "model_name": "test-model",
                "prompt": "test-prompt",
                "cpu": 5000,
                "memory": 8192,
                "gpu_count": 1,
            },
        )
        self.assertEqual(dispatch_response.status_code, 200)

        # 3. Poll the victim job's allocations for preemption
        for _ in range(30): # 30 seconds timeout
            allocs = self.nomad.job.get_allocations(self.victim_job_name)
            if allocs and allocs[0]["ClientStatus"] == "complete" and "Preempted" in allocs[0]["Events"][0]["Message"]:
                break
            time.sleep(1)
        else:
            self.fail("Victim job was not preempted within the timeout")

if __name__ == "__main__":
    unittest.main()
