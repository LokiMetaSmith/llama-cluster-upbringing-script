variable "model_path" {
  type        = string
  description = "The absolute path to the GGUF model file to benchmark."
  default     = "/path/to/default/model.gguf"
}

job "llama-benchmark" {
  datacenters = ["dc1"]
  type        = "batch"

  group "benchmark-group" {
    count = 1

    task "benchmark-task" {
      driver = "exec"

      template {
        data = <<EOH
#!/bin/bash
API_SERVER=$(nomad service discover -address-type=ipv4 llama-api | head -n 1)

/home/user/llama.cpp/build/bin/llama-bench \\
  -m ${var.model_path} \\
  -p 512 \\
  -n 512 \\
  --api-key "dummy" \\
  --host $API_SERVER
EOH
        destination = "local/run_benchmark.sh"
        perms       = "0755"
      }

      config {
        command = "local/run_benchmark.sh"
      }
    }
  }
}
