job "munder-difflin" {
  datacenters = ["dc1"]
  type        = "service"

  group "harness" {
    count = 1

    network {
      port "http" {
        to = 3000
      }
      port "hooks" {
        to = 8888
      }
    }

    volume "unified_fs" {
      type      = "host"
      read_only = false
      source    = "unified_fs"
    }

    task "munder-difflin-agent" {
      driver = "docker"

      config {
        image = "node:20-slim"
        command = "bash"
        args = [
          "-c",
          "apt-get update && apt-get install -y git python3 build-essential && npm install -g munder-difflin && munder-difflin --headless --port 3000"
        ]

        ports = ["http", "hooks"]
      }

      volume_mount {
        volume      = "unified_fs"
        destination = "/data/hive"
        read_only   = false
      }

      env {
        HIVE_ROOT         = "/data/hive"
        NODE_ENV          = "production"
        LOG_LEVEL         = "info"
        CONSUL_HTTP_ADDR  = "${attr.unique.network.ip-address}:8500"
      }

      resources {
        cpu    = 1000
        memory = 2048
      }

      service {
        name = "munder-difflin-harness"
        port = "http"

        check {
          type     = "http"
          path     = "/health"
          interval = "10s"
          timeout  = "2s"
        }
      }
    }
  }
}
