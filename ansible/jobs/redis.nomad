job "redis" {
  datacenters = ["dc1"]
  type      = "service"
  priority  = 80

  update {
    max_parallel      = 1
    min_healthy_time = "30s"
    healthy_deadline = "5m"
  }

  group "redis" {
    volume "redis_data" {
      type      = "host"
      read_only = false
      source    = "redis_data"
    }

    network {
      mode = "bridge"
      port "redis" {
        to = 6379
      }
    }

    task "redis" {
      driver = "docker"

      volume_mount {
        volume      = "redis_data"
        destination = "/data"
        read_only   = false
      }

      config {
        image = "redis:7.2-alpine"
        command = "redis-server"
        args    = ["--appendonly", "yes"]
      }
      service {
        name = "redis"
        port = "redis"
        connect {
          sidecar_service {
            port = "6379"
          }
        }
        check {
          type     = "tcp"
          interval = "10s"
          timeout  = "2s"
        }
      }
      resources {
        cpu    = 100
        memory = 128
      }
    }
  }
}
