job "rag-service" {
  datacenters = ["dc1"]
  type = "service"

  group "rag-group" {
    count = 1

    network {
      mode = "bridge"
      port "http" {
        to = 8000
      }
    }

    service {
      name = "rag-service"
      port = "8000"

      connect {
        sidecar_service {}
      }

      check {
        name     = "RAG Service HTTP Check"
        type     = "http"
        path     = "/docs"
        interval = "10s"
        timeout  = "2s"
      }
    }

    task "rag-server" {
      driver = "docker"

      config {
        image = "rag-service:local"
        ports = ["http"]
      }

      env {
        PORT = "8000"
        # Mount the repository if needed, or rely on internal knowledge base
        RAG_BASE_DIR = "/repo"
        RAG_ALLOW_ROOT_SCAN = "True"
      }

      resources {
        cpu    = 1000 # 1000 MHz
        memory = 2048 # 2GB RAM for embedding models
      }
    }
  }
}
