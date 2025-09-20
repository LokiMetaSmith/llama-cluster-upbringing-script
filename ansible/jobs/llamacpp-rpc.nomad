job "llamacpp-rpc" {
  datacenters = ["dc1"]
  namespace   = "default"

  group "workers" {
    count = 2 # Default to 2 workers, can be scaled

    network {
      mode = "bridge"
      port "rpc" {}
    }

    service {
      name     = "llama-cpp-rpc-worker"
      provider = "consul"
      port     = "rpc"

      check {
        type     = "tcp"
        interval = "15s"
        timeout  = "5s"
      }
    }

    task "rpc-server" {
      driver = "exec"

      template {
        data = <<EOH
#!/bin/bash
set -e
echo "Starting RPC server..."
/usr/local/bin/rpc-server --host 0.0.0.0 --port {{ '{{' }} env "NOMAD_PORT_rpc" {{ '}}' }}
EOH
        destination = "local/run_rpc_server.sh"
        perms       = "0755"
      }

      config {
        command = "local/run_rpc_server.sh"
      }

      resources {
        cpu    = 500
        memory = 1024
      }
    }
  }
}
