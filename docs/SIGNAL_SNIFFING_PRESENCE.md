# Signal Sniffing Presence Intelligence Architecture

This document details the signal sniffing presence intelligence module integrated into `services/tap_orchestrator/`. It extends the physical cryptographic challenge-response daemon (UWB/ESP32) with passive radio-frequency (RF), Wi-Fi promiscuous, and Software-Defined Radio (SDR) signal intelligence to continuously monitor ambient spatial presence.

## Overview

Physical presence detection in the cluster uses a two-tier approach:
1. **Active Cryptographic Verification (Tier 1):** UWB/NFC tokens signed via ECDSA (see `docs/PROXIMITY_CHALLENGE_DAEMON.md`).
2. **Passive RF Signal Intelligence (Tier 2):** Continuous Wi-Fi promiscuous packet sniffing and wideband SDR RF energy monitoring (e.g. BirriaSDR / MT7921 / ESP32 promiscuous mode) to passively sense ambient device proximity, spatial density, and movement.

This passive layer allows the cluster to dynamically scale compute priority and prepare agent workers in rooms before an explicit active cryptographic tap occurs.

## System Architecture & Data Flow

```
+------------------------------------+      +-----------------------------------+
|  ESP32 Wi-Fi Promiscuous Sniffer   |      |  Wi-Fi SDR Receiver (BirriaSDR)   |
| (Probe Requests / RSSI / Channel) |      |   (40 MSps Raw IQ / Power Level)  |
+------------------------------------+      +-----------------------------------+
                  |                                           |
                  +---------------------+---------------------+
                                        | HTTP POST /api/v1/telemetry/rf
                                        v
                    +---------------------------------------+
                    |           Tap Orchestrator            |
                    |     (services/tap_orchestrator/)      |
                    +---------------------------------------+
                                        |
                                        v
                    +---------------------------------------+
                    |           RFSnifferEngine             |
                    |   - MAC Hashing / Anonymization       |
                    |   - RSSI Signal Normalization         |
                    |   - Spatial Presence Scoring          |
                    +---------------------------------------+
                                   /         \
                                  /           \
                                 v             v
            +-------------------------+   +----------------------------+
            |  Datalog REA Ledger     |   |   Consul KV Fast State     |
            |  assert_fact("rf_...")  |   | compute_rights/rf_<room>   |
            +-------------------------+   +----------------------------+
```

## REST API Endpoint

### `POST /api/v1/telemetry/rf`

Submits an RF telemetry frame containing batched RSSI and packet samples from a sniffing sensor node.

**Request Body (`RFTelemetryFrame`):**
```json
{
  "sensor_id": "esp32-sniffer-node-01",
  "room_id": "room_101",
  "timestamp": 1713200000.0,
  "samples": [
    {
      "device_id": "a4:c3:f0:12:34:56",
      "rssi": -62,
      "channel": 6,
      "frame_type": "probe_request",
      "snr": 18.5
    }
  ]
}
```

**Response (`RFPresenceResponse`):**
```json
{
  "status": "success",
  "processed_samples": 1,
  "active_devices_detected": 1,
  "allocated_weight": 21.88
}
```

## Privacy & Anonymization

To preserve privacy and prevent persistent tracking of unauthenticated device MAC addresses:
- The `RFSnifferEngine` cleans and converts incoming raw MAC addresses into 16-character SHA-256 hashes (`anonymize_device_id`).
- Raw MAC addresses are never stored in the Datalog REA ledger or propagated to Consul KV state.

## RSSI Signal Normalization & Presence Scoring

1. **RSSI Thresholding:** Samples with RSSI lower than `-90 dBm` are discarded as background noise.
2. **Normalized Confidence:** Signal strength is mapped linearly between `-90 dBm` (0.0 confidence) and `-30 dBm` (1.0 confidence).
3. **Composite Room Weight:** Active device confidence scores are aggregated and scaled to yield a composite room compute weight (`compute_rights/rf_<room_id>`).

## Hardware Integration Examples

1. **ESP32 Promiscuous Sniffer:**
   - Reference implementation available at `examples/proximity_hardware_reference/esp32_wifi_sniffer.ino`.
   - Uses ESP-IDF `esp_wifi_set_promiscuous()` to intercept IEEE 802.11 management/data headers.
2. **Wi-Fi SDR Receiver (BirriaSDR / MT7921 / MT7961):**
   - Dongles running `libbirriasdr` capture wideband 40 MSps raw I/Q samples to analyze ambient RF energy and probe bursts across 2.4 GHz channels (2156–2610 MHz).
