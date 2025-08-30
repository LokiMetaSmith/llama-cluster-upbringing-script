variable "job_name" {
  type        = string
  description = "A unique name for the job."
  default     = "prima-cluster"
}

variable "service_name" {
  type        = string
  description = "The name of the Consul service for the prima master."
  default     = "prima-master"
}

variable "model_path" {
  type        = string
  description = "The absolute path to the GGUF model file."
  default     = "/path/to/default/model.gguf"
}

variable "node_count" {
  type        = number
  description = "The number of nodes to run in the prima.cpp cluster."
  default     = 1
}

job "${var.job_name}" {
  datacenters = ["dc1"]
  type        = "service"

  group "prima-nodes" {
    count = var.node_count

    network {
      port "http" {}
    }

    service {
      name     = var.service_name
      provider = "consul"
      port     = "http"

      connect {
        sidecar_service {}
      }
    }

    task "prima-cli" {
      driver = "raw_exec"

      template {
        data = <<EOH
#!/bin/bash
MASTER_IP=$(nomad service discover -address-type=ipv4 ${var.service_name} | head -n 1)
NEXT_IP=$(nomad service discover -address-type=ipv4 ${var.service_name} | head -n 1) # Simplified for single node

/home/user/prima.cpp/build/bin/llama-cli \\
  --model ${var.model_path} \\
  --world ${var.node_count} \\
  --rank ${NOMAD_ALLOC_INDEX} \\
  --master $MASTER_IP \\
  --next $NEXT_IP
EOH
        destination = "local/run.sh"
        perms       = "0755"
      }

      config {
        command = "local/run.sh"
      }
    }
  }
}
