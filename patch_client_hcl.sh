#!/bin/bash
cat << 'HCL' >> append_volumes.hcl

  host_volume "influxdb-data" {
    path      = "{{ nomad_volumes_dir }}/influxdb-data"
    read_only = false
  }

  host_volume "openclaw-config" {
    path      = "{{ nomad_volumes_dir }}/openclaw-config"
    read_only = false
  }

  host_volume "openclaw-data" {
    path      = "{{ nomad_volumes_dir }}/openclaw-data"
    read_only = false
  }

  host_volume "cluster-infra" {
    path      = "{{ nomad_volumes_dir }}/cluster-infra"
    read_only = true
  }

  host_volume "mcp-config" {
    path      = "{{ nomad_volumes_dir }}/mcp-config"
    read_only = false
  }
HCL

sed -i '/host_volume "radicle_data" {/,+4r append_volumes.hcl' ansible/roles/nomad/templates/client.hcl.j2
sed -i '/host_volume "radicle_data" {/,+4r append_volumes.hcl' ansible/roles/nomad/templates/server.hcl.j2
rm append_volumes.hcl
