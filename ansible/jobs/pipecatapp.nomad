job "pipecat-app" {
  datacenters = ["dc1"]
  type        = "service"

  group "pipecat-group" {
    count = 1

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
        interval = "10s"
        timeout  = "2s"
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

      logs {
        max_files     = 3
        max_file_size = 10 # MB
      }

      resources {
        cpu    = 1000 # 1 GHz
        memory = 1024 # 4 GB
      }
    }
  }
}
