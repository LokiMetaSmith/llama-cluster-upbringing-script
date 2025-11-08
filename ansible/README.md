# Ansible

This directory contains all Ansible playbooks, roles, and templates for provisioning and deploying the entire system.

## Directory Structure

- **filter_plugins**: Custom Ansible filter plugins.
- **jobs**: Ansible jobs to be run by Nomad.
- **paddler_agent**: An Ansible role for the paddler agent.
- **paddler_balancer**: An Ansible role for the paddler balancer.
- **roles**: Individual, reusable components for managing specific parts of the system.
- **tasks**: Individual tasks that can be included in plays.
