job "dummy-web-service" {
  datacenters = ["dc1"]
  type = "service"

  group "web" {
    count = 3 # Run multiple instances to test load balancing across nodes

    network {
      port "http" {
        to = 8000
      }
    }

    service {
      name = "dummy-web"
      port = "http"

      # Register with Traefik for load balancing
      tags = []

      check {
        type     = "http"
        path     = "/"
        interval = "10s"
        timeout  = "2s"
      }
    }

    task "server" {
      driver = "docker"

      config {
        image = "python:3.9-slim"
        # Create a simple python web server that returns the node ID it's running on
        command = "sh"
        args = [
          "-c",
          "echo \"import http.server, socketserver, os; class MyHandler(http.server.SimpleHTTPRequestHandler): def do_GET(self): self.send_response(200); self.send_header('Content-type', 'text/plain'); self.end_headers(); self.wfile.write(f'Node: {os.environ.get(\\\"node.unique.id\\\", \\\"unknown\\\")} | Alloc: {os.environ.get(\\\"NOMAD_ALLOC_ID\\\", \\\"unknown\\\")} \\n'.encode('utf-8')); httpd = socketserver.TCPServer(('', 8000), MyHandler); httpd.serve_forever()\" > server.py && python server.py"
        ]
        ports = ["http"]
      }

      env {
        "node.unique.id" = "${node.unique.id}"
      }

      resources {
        cpu    = 50 # 50 MHz
        memory = 64 # 64 MB
      }
    }
  }
}
