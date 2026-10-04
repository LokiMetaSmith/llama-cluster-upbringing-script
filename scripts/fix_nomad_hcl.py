import re

with open("/etc/nomad.d/server.hcl", "r") as f:
    text = f.read()

# Remove any corrupted lines
text = re.sub(r"nplugin containerd-driver [^\n]*", "", text)
text = re.sub(r'plugin "containerd-driver"\s*\{.*?\}', "", text, flags=re.DOTALL)

plugin_stanza = """
plugin "containerd-driver" {
  config {
    enabled = true
    containerd_runtime = "io.containerd.runc.v2"
  }
}
"""

final_text = text.strip() + "\n" + plugin_stanza

with open("/etc/nomad.d/server.hcl", "w") as f:
    f.write(final_text)

print("Updated /etc/nomad.d/server.hcl successfully")
