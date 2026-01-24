job "immich" {
  datacenters = ["dc1"]
  type        = "service"

  group "immich" {
    count = 1

    network {
      mode = "bridge"
      port "http" {
        to = 2283
      }
    }

    service {
      name = "immich"
      port = "http"
      check {
        type     = "http"
        path     = "/api/server-info/ping"
        interval = "10s"
        timeout  = "2s"
      }
    }

    # --- Database (Postgres) ---
    task "database" {
      driver = "docker"

      config {
        image = "tensorchord/pgvecto-rs:pg14-v0.2.0"
        volumes = [
          "/opt/nomad/volumes/immich-postgres:/var/lib/postgresql/data"
        ]
      }

      env {
        POSTGRES_PASSWORD = "postgres" # Change in production
        POSTGRES_USER     = "postgres"
        POSTGRES_DB       = "immich"
      }

      resources {
        cpu    = 500
        memory = 512
      }
    }

    # --- Redis ---
    task "redis" {
      driver = "docker"

      config {
        image = "redis:6.2-alpine"
      }

      resources {
        cpu    = 100
        memory = 128
      }
    }

    # --- Immich Server ---
    task "immich-server" {
      driver = "docker"

      config {
        image = "ghcr.io/immich-app/immich-server:release"
        ports = ["http"]
        volumes = [
          "/opt/nomad/volumes/immich-upload:/usr/src/app/upload",
          "/etc/localtime:/etc/localtime:ro"
        ]
      }

      env {
        DB_HOSTNAME = "127.0.0.1" # Bridge networking allows localhost communication
        DB_USERNAME = "postgres"
        DB_PASSWORD = "postgres"
        DB_DATABASE_NAME = "immich"
        REDIS_HOSTNAME = "127.0.0.1"
      }

      resources {
        cpu    = 1000
        memory = 2048
      }
    }

    # --- Immich Machine Learning ---
    task "immich-machine-learning" {
      driver = "docker"

      config {
        image = "ghcr.io/immich-app/immich-machine-learning:release"
        volumes = [
          "/opt/nomad/volumes/immich-cache:/cache"
        ]
      }

      resources {
        cpu    = 1000
        memory = 2048
      }
    }
  }
}
