job "pipecat-app" {
  datacenters = ["dc1"]
  type        = "service"

  group "pipecat-group" {
    count = 1

    network {
      port "http" {
        to = 8000
      }
    }

    task "pipecat-task" {
      driver = "exec"

      config {
        command = "python3"
        args    = ["/home/user/app.py"]
      }
    }
  }
}
