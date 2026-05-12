import re

with open('README.md', 'r') as f:
    content = f.read()

# The actual line in README.md might be slightly different. Let's just find "Monitoring and Observability" and make it checked
# Currently it looks like: "- **Monitoring and Observability:** Deploy a monitoring stack like Prometheus and Grafana to collect and visualize metrics from Nomad, Consul, and the application itself."

updated_content = content.replace(
    "- **Monitoring and Observability:** Deploy a monitoring stack like Prometheus and Grafana to collect and visualize metrics from Nomad, Consul, and the application itself.",
    "- [x] **Monitoring and Observability:** Deploy a monitoring stack like Prometheus and Grafana to collect and visualize metrics from Nomad, Consul, and the application itself."
)

with open('README.md', 'w') as f:
    f.write(updated_content)

print("Updated README.md")
