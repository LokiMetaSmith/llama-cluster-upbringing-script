job "prima-cluster-{{ meta.JOB_NAME | default \"default\" }}" {
  datacenters = ["dc1"]
  type        = "service"
  namespace   = "{{ meta.NAMESPACE | default \"default\" }}"

  meta {
    NAMESPACE     = "default"
    JOB_NAME      = "default"
    SERVICE_NAME  = "prima-master-default"
    MODEL_PATH    = "/path/to/your/default/model.gguf"
    NODE_COUNT    = "1"
  }

  group "prima-nodes" {
    count = meta.NODE_COUNT

    task "prima-cli" {
      driver = "raw_exec"

      template {
        data = <<EOH
#!/bin/bash
MASTER_IP=$(nomad service discover -address-type=ipv4 {{ meta.SERVICE_NAME }} | head -n 1)
NEXT_IP=$(nomad service discover -address-type=ipv4 {{ meta.SERVICE_NAME }} | head -n 1) # Simplified for single node

/home/user/prima.cpp/build/bin/llama-cli \
  --model {{ meta.MODEL_PATH }} \
  --world {{ meta.NODE_COUNT }} \
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
        name = meta.SERVICE_NAME
        port = "8080"

        connect {
          sidecar_service {}
        }

        check {
          type     = "tcp"
          interval = "10s"
          timeout  = "2s"
        }
      }
    }
  }
}
