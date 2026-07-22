# Cybersecurity Implementation Plan: Lightweight Swarm Security

## 1. Executive Summary

This document outlines the implementation plan for introducing lightweight cybersecurity monitoring and anomaly detection to the AI cluster. The objective is to give the AI agent swarm self-awareness of its security state without overwhelming the legacy hardware (Intel Core 2 Duo, limited RAM/compute).

We will rely on rule-based heuristics and lightweight statistical anomaly detection applied to Nomad logs, Consul logs, and the internal MQTT communication bus. Alerts will be published back to the MQTT bus for the swarm to ingest and react to.

## 2. Architecture Overview

The security architecture is designed to be frugal and decentralized, consisting of three main components:

1. **Data Collection (Log Aggregation):** Lightweight log shipping of Nomad, Consul, and system logs.
2. **Anomaly Detection Engine:** A low-overhead Python service running on the cluster that evaluates rules and detects anomalies.
3. **Messaging & Swarm Integration:** An MQTT topic structure dedicated to security alerts, consumed by the existing AI agents.

## 3. Tool Selection & Implementation Details

### 3.1. Log Aggregation: Vector or Fluent Bit

To avoid heavy Java-based or ELK-stack collectors, we recommend deploying a lightweight log forwarder.

* **Vector (by Datadog)** or **Fluent Bit** are both excellent choices.
* **Implementation:** Deploy as a Nomad system job (`type = "system"`) to ensure it runs on every node. It will tail `/var/log/syslog`, Nomad allocation logs, and Consul logs, filtering for critical error patterns and authentication failures, then forwarding them to the Anomaly Detection Engine.

### 3.2. Anomaly Detection Engine: Lightweight Python Service

Instead of deploying a resource-heavy AI model or a complex SIEM, we will build a custom, lightweight Python service managed by Nomad.

* **Core Logic:**
  * **Rule-Based Heuristics:** Use simple regex and threshold counters to detect known bad behavior (e.g., repeated authentication failures, unauthorized Consul KV writes, unknown Nomad job submissions).
  * **Statistical Anomalies:** Use a lightweight library like `PyOD` (Python Outlier Detection) or simple moving averages to detect spikes in MQTT message frequency, unusual log volumes, or sudden CPU/Memory spikes that indicate resource exhaustion attacks.
* **Implementation:** Deploy as a Nomad job (`security-agent.nomad`). It will consume the aggregated logs, parse the internal MQTT traffic, and run the detection logic on a fixed interval.

### 3.3. Messaging and Alerting via MQTT

The cluster's existing MQTT broker (e.g., Mosquitto) will be the backbone of the security alerting system.

* **Topic Structure:** Introduce a new topic namespace for security:
  * `cluster/security/alerts/high` - Critical issues (e.g., node compromise, unauthorized access).
  * `cluster/security/alerts/low` - Warnings (e.g., high failed login rate, log volume spikes).
  * `cluster/security/heartbeat` - To ensure the security agent itself is running.
* **Implementation:** The Anomaly Detection Engine publishes JSON-formatted alert payloads to these topics.

### 3.4. AI Swarm Integration

The existing agent swarm needs to consume these alerts and incorporate them into its context.

* **Implementation:**
  * Update the `TwinService` or Worker Agents to subscribe to `cluster/security/alerts/#`.
  * When an alert is received, it should be injected into the agent's short-term memory or prompt context (e.g., "SYSTEM ALERT: Unusual activity detected on node worker2").
  * *Future Iteration:* The agents can use existing tools (like the `ansible` or `nomad` tools) to take automated remediation actions, such as isolating a compromised allocation.

## 4. Phase-by-Phase Rollout Plan

### Phase 1: Foundational Visibility

1. **Deploy Log Forwarder:** Create and deploy a Nomad system job for Fluent Bit/Vector. Configure it to tail Consul and Nomad logs.
2. **Define MQTT Topics:** Standardize the `cluster/security/alerts/#` schema.

### Phase 2: Lightweight Rule-Based Detection

1. **Develop Security Agent:** Write a Python script (`security_agent.py`) that subscribes to the log stream and MQTT bus.
2. **Implement Heuristics:** Add basic rules (e.g., >5 failed logins in 1 minute, unknown MQTT topics).
3. **Publish Alerts:** Configure the agent to publish findings to the MQTT alerts topic.
4. **Deploy via Nomad:** Package the agent in a Docker container and deploy it via Nomad to a core node.

### Phase 3: Swarm Awareness

1. **Agent Integration:** Modify the core `pipecatapp` workflows to subscribe to the security MQTT topics.
2. **Context Injection:** Ensure alerts gracefully interrupt or append to the agent's current context without breaking conversational flow.
3. **Testing:** Simulate attacks (e.g., spamming the MQTT bus, failing SSH logins) and verify the swarm acknowledges the alert.

### Phase 4: Advanced Anomaly Detection (Future)

1. **Statistical Baselines:** Introduce `PyOD` to establish baselines for "normal" cluster behavior (log velocity, message frequency).
2. **Automated Response:** Grant the agent swarm permissions to quarantine nodes or restart services based on specific high-confidence alerts.

## 5. Security & Resource Considerations

* **Resource Caps:** The `security-agent` Nomad job must have strict CPU and memory limits (`resources { memory = 128, cpu = 200 }`) to prevent it from starving the LLM inferences on legacy hardware.
* **Self-Monitoring:** The security agent must emit a heartbeat to ensure it hasn't been disabled by a malicious actor or a system crash.
* **No Heavy ML:** Stick strictly to heuristics and lightweight math. General-purpose LLMs should *not* be used for log parsing on this hardware tier.
