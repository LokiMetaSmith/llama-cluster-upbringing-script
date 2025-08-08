job "llamacpp-rpc" {
  datacenters = ["dc1"]

  group "master" {
    count = 1

    task "llama-master" {
      driver = "exec"

      template {
        data = <<EOH
#!/bin/bash
WORKER_IPS=$(nomad service discover -address-type=ipv4 llama-rpc-worker | tr '\n' ',' | sed 's/,$//')

/home/user/llama.cpp/build/bin/llama-server \
  --model /path/to/your/model.gguf \
  --host 0.0.0.0 \
  --port 8080 \
  --rpc-servers $WORKER_IPS
EOH
        destination = "local/run_master.sh"
        perms       = "0755"
      }

      config {
        command = "local/run_master.sh"
      }

      service {
        name = "llama-api"
        port = "8080"

        check {
          type     = "tcp"
          interval = "10s"
          timeout  = "2s"
        }
      }
    }
  }

  group "workers" {
    count = 2 # Should be (number of nodes) - 1

    task "llama-worker" {
      driver = "exec"

      config {
        command = "/home/user/llama.cpp/build/bin/llama-server"
        args = [
          "--model", "/path/to/your/model.gguf",
          "--host", "0.0.0.0",
          "--port", "8081", # Use a different port for workers
        ]
      }

      service {
        name = "llama-rpc-worker"
        port = "8081"
      }
    }
  }
}
