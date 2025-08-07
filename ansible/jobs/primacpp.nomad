job "prima-cluster" {
  datacenters = ["dc1"]
  type        = "service"

  group "prima-nodes" {
    count = 1

    task "prima-cli" {
      driver = "raw_exec"

      template {
        data = <<EOH
#!/bin/bash
MASTER_IP=$(nomad service discover -address-type=ipv4 prima-master | head -n 1)
NEXT_IP=$(nomad service discover -address-type=ipv4 prima-master | head -n 1) # Simplified for single node

/home/user/prima.cpp/build/bin/llama-cli \
  --model /path/to/your/model.gguf \
  --world 1 \
  --rank ${NOMAD_ALLOC_INDEX} \
  --master $MASTER_IP \
  --next $NEXT_IP
EOH
        destination = "local/run.sh"
        perms       = "0755"
      }

      config {
        command = "local/run.sh"
      }

      service {
        name = "prima-master"
        port = "8080"

        check {
          type     = "tcp"
          interval = "10s"
          timeout  = "2s"
        }
      }
    }
  }
}
