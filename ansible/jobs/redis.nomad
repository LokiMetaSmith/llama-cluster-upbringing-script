# Consul Connect Service Mesh Configuration
#
# To enable Consul Connect sidecar for service mesh:
# 1. Ensure Consul is configured with connect.enabled = true
# 2. The sidecar_service block enables automatic mTLS between services
# 3. Upstream services can connect via localhost:<mappedPort>
#    (Consul Connect handles the routing automatically)
#
# NOTE: This feature requires:
# - Consul 1.6+ with Connect enabled
# - Nomad 0.9+ with connect plugin
# - Proper ACL tokens for Connect
#
job "redis" {
  datacenters = ["dc1"]
  type      = "service"

  update {
    max_parallel      = 1
    min_healthy_time = "30s"
    healthy_deadline = "5m"
  }

  group "redis" {
    network {
      mode = "bridge"
      port "redis" {
        to = 6379
      }
    }

    task "redis" {
      driver = "docker"
      config {
        image = "redis:7.2-alpine"
      }
      service {
        name = "redis"
        port = "redis"
        connect {
          sidecar_service {
            # Enable Consul Connect sidecar
            # This allows automatic service mesh capabilities
            # including mTLS between services
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