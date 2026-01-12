job "pipecat-app" {
  datacenters = ["dc1"]
  type        = "service"

  group "pipecat-group" {
    count = 3

    update {
      max_parallel = 1
      min_healthy_time = "10s"
      healthy_deadline = "3m"
      auto_revert = true
    }

    migrate {
      max_parallel = 1
      health_check = "checks"
      healthy_deadline = "5m"
    }

    reschedule {
      attempts  = 3
      interval  = "2m"
      delay     = "30s"
      unlimited = false
    }

    network {
      mode = "host"
      port "http" {
        to = 8000
      }
    }

    volume "snd" {
      type   = "host"
      source = "snd"
    }

    service {
      name = "pipecat-app-http"
      port = "http"
      provider = "consul"

      check {
        type     = "http"
        path     = "/health"
        interval = "30s"
        timeout  = "10s"
        initial_delay = "10m"
      }

    }

    task "pipecat-task" {
      driver = "raw_exec"

      config {
        command = "/opt/pipecatapp/start_pipecat.sh"
      }



      volume_mount {
        volume      = "snd"
        destination = "/dev/snd"
       read_only   = false
      }



      resources {
        cpu    = 1000 # 1 GHz
        memory = 1024 # 4 GB
      }
    }
  }
}
