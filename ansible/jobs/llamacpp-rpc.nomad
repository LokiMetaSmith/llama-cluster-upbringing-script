job "llamacpp-rpc" {
  datacenters = ["dc1"]
  namespace   = "default"

  group "master" {
    count = 1

    network {
      mode = "bridge"
      port "http" {}
    }

    service {
      name     = "llama-cpp-api"
      provider = "consul"
      port     = "http"


      check {
          type     = "http"
          path     = "/"
          interval = "10s"
          timeout  = "2s"

      }
    }

    volume "models" {
      type      = "host"
      read_only = true
      source    = "/opt/nomad/models"
    }

    task "llama-master" {
      driver = "exec"

      template {
        data = <<EOH
#!/bin/bash
echo "Hello from run_master.sh" > /tmp/master-script.log
exit 1
EOH
        destination = "local/run_master.sh"
        perms       = "0755"
      }

      config {
        command = "local/run_master.sh"
      }

      resources {
        cpu    = 1000
        memory = {% if llm_models_var[0].memory_mb is defined %}{{ llm_models_var[0].memory_mb }}{% else %}2048{% endif %}

      }

      volume_mount {
        volume      = "models"
        destination = "/opt/nomad/models"
        read_only   = true
      }
    }
  }

  group "workers" {
    count = {% if llm_models_var[0].WORKER_COUNT is defined %}{{ llm_models_var[0].WORKER_COUNT }}{% else %}1{% endif %}

    network {
      mode = "bridge"
      port "rpc" {}
    }

    service {
      name     = "llama-cpp-rpc-worker"
      provider = "consul"
      port     = "rpc"
    }

    volume "models" {
      type      = "host"
      read_only = true
      source    = "/opt/nomad/models"
    }

    task "llama-worker" {
      driver = "exec"

      template {
        data = <<EOH
#!/bin/bash
/usr/local/bin/llama-server \
  --model "/opt/nomad/models/llm/{{ llm_models_var[0].filename }}" \
  --host 0.0.0.0 \
  --port {{ '{{' }} env "NOMAD_PORT_rpc" {{ '}}' }}
EOH
        destination = "local/run_worker.sh"
        perms       = "0755"
      }

      config {
        command = "local/run_worker.sh"
      }

      resources {
        cpu    = 1000
        memory = {% if llm_models_var[0].memory_mb is defined %}{{ llm_models_var[0].memory_mb }}{% else %}2048{% endif %}

      }

      volume_mount {
        volume      = "models"
        destination = "/opt/nomad/models"
        read_only   = true
      }
    }
  }
}
