job "test-worker-task" {
  datacenters = ["dc1"]
  type        = "batch"

  constraint {
    attribute = "${node.unique.name}"
    value     = "pipecat-1-worker"
  }

  task "probe" {
    driver = "raw_exec"

    config {
      command = "/bin/bash"
      args    = ["-c", "echo TASK_SUCCESS: Executed on $(hostname) with IP $(hostname -I) at $(date)"]
    }

    resources {
      cpu    = 100
      memory = 64
    }
  }
}
