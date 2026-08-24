job "pihole" {
  datacenters = ["dc1"]
  type        = "service"

  group "pihole" {
    count = 1

    network {
      port "dns_tcp" {
        static = 53
        to     = 53
      }
      port "dns_udp" {
        static = 53
        to     = 53
      }
      port "web" {
        to = 80
      }
    }

    volume "pihole_data" {
      type      = "host"
      read_only = false
      source    = "pihole_data"
    }

    volume "dnsmasq_data" {
      type      = "host"
      read_only = false
      source    = "dnsmasq_data"
    }

    service {
      name = "pihole-web"
      port = "web"

      tags = [
        "traefik.enable=true",
        "traefik.http.routers.pihole.rule=Host(`pihole.local`)",
        "traefik.http.routers.pihole.entrypoints=web"
      ]

      check {
        type     = "http"
        path     = "/admin/index.php"
        interval = "15s"
        timeout  = "3s"
      }
    }

    service {
      name = "pihole-dns"
      port = "dns_udp"

      check {
        type     = "tcp"
        interval = "10s"
        timeout  = "2s"
      }
    }

    task "pihole" {
      driver = "docker"

      config {
        image = "pihole/pihole:latest"
        ports = ["dns_tcp", "dns_udp", "web"]
      }

      volume_mount {
        volume      = "pihole_data"
        destination = "/etc/pihole"
        read_only   = false
      }

      volume_mount {
        volume      = "dnsmasq_data"
        destination = "/etc/dnsmasq.d"
        read_only   = false
      }

      env {
        TZ           = "UTC"
        WEBPASSWORD  = "admin"
        FTLCONF_LOCAL_IPV4 = "127.0.0.1"
      }

      resources {
        cpu    = 500
        memory = 512
      }
    }
  }
}
