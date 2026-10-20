/**
 * ESP32 Wi-Fi Promiscuous Sniffer Reference Implementation
 *
 * Demonstrates an ESP32 operating in Wi-Fi promiscuous mode to passively sniff
 * ambient Wi-Fi packets (probe requests, beacon frames, packet headers) and transmit
 * RSSI & device signal telemetry frames to the Tap Orchestrator REST endpoint.
 *
 * Target Endpoint: POST /api/v1/telemetry/rf
 *
 * Dependencies:
 * - ArduinoJson (v6+)
 * - WiFi / HTTPClient (ESP32 core)
 * - esp_wifi.h (ESP-IDF Wi-Fi promiscuous driver API)
 */

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "esp_wifi.h"

const char* WIFI_SSID = "YOUR_SSID";
const char* WIFI_PASSWORD = "YOUR_PASSWORD";
const char* TELEMETRY_URL = "http://192.168.1.100:8011/api/v1/telemetry/rf";
const char* ROOM_ID = "room_101";
const char* SENSOR_ID = "esp32-sniffer-node-01";

// Buffer for storing detected RF signal samples
struct PacketSample {
    char mac[18];
    int rssi;
    int channel;
    char frame_type[16];
};

#define MAX_SAMPLES 10
PacketSample sample_buffer[MAX_SAMPLES];
volatile int sample_count = 0;
portMUX_TYPE sampleMux = portMUX_INITIALIZER_UNLOCKED;

// Wi-Fi Promiscuous Callback
void promiscuous_rx_cb(void* buf, wifi_promiscuous_pkt_type_t type) {
    wifi_promiscuous_pkt_t* pkt = (wifi_promiscuous_pkt_t*)buf;
    wifi_pkt_rx_ctrl_t rx_ctrl = pkt->rx_ctrl;

    // Filter out weak packets
    if (rx_ctrl.rssi < -90) {
        return;
    }

    // Extract IEEE 802.11 MAC header (Transmitter Address / Source Address)
    // Frame control bytes: offset 0-1. Address 2 (Transmitter Address): offset 10-15
    const uint8_t* payload = pkt->payload;
    if (pkt->rx_ctrl.sig_len < 24) return;

    uint8_t mac_bytes[6];
    memcpy(mac_bytes, &payload[10], 6);

    // Skip broadcast or null MACs
    if (mac_bytes[0] == 0xFF && mac_bytes[1] == 0xFF) return;

    portENTER_CRITICAL_ISR(&sampleMux);
    if (sample_count < MAX_SAMPLES) {
        snprintf(sample_buffer[sample_count].mac, sizeof(sample_buffer[sample_count].mac),
                 "%02x:%02x:%02x:%02x:%02x:%02x",
                 mac_bytes[0], mac_bytes[1], mac_bytes[2],
                 mac_bytes[3], mac_bytes[4], mac_bytes[5]);

        sample_buffer[sample_count].rssi = rx_ctrl.rssi;
        sample_buffer[sample_count].channel = rx_ctrl.channel;

        if (type == WIFI_PKT_MGMT) {
            uint8_t frame_sub_type = (payload[0] >> 4) & 0x0F;
            if (frame_sub_type == 4) {
                strncpy(sample_buffer[sample_count].frame_type, "probe_request", 16);
            } else {
                strncpy(sample_buffer[sample_count].frame_type, "mgmt_frame", 16);
            }
        } else {
            strncpy(sample_buffer[sample_count].frame_type, "data_frame", 16);
        }

        sample_count++;
    }
    portEXIT_CRITICAL_ISR(&sampleMux);
}

void sendTelemetry() {
    portENTER_CRITICAL(&sampleMux);
    int count = sample_count;
    if (count == 0) {
        portEXIT_CRITICAL(&sampleMux);
        return;
    }

    StaticJsonDocument<1024> doc;
    doc["sensor_id"] = SENSOR_ID;
    doc["room_id"] = ROOM_ID;
    doc["timestamp"] = (double)millis() / 1000.0;

    JsonArray samples = doc.createNestedArray("samples");
    for (int i = 0; i < count; i++) {
        JsonObject obj = samples.createNestedObject();
        obj["device_id"] = sample_buffer[i].mac;
        obj["rssi"] = sample_buffer[i].rssi;
        obj["channel"] = sample_buffer[i].channel;
        obj["frame_type"] = sample_buffer[i].frame_type;
    }
    sample_count = 0;
    portEXIT_CRITICAL(&sampleMux);

    String requestBody;
    serializeJson(doc, requestBody);

    // Disable promiscuous mode briefly during HTTP transmission
    esp_wifi_set_promiscuous(false);

    HTTPClient http;
    http.begin(TELEMETRY_URL);
    http.addHeader("Content-Type", "application/json");

    int httpCode = http.POST(requestBody);
    if (httpCode == 200) {
        Serial.printf("[Telemetry] Posted %d RF samples successfully\n", count);
    } else {
        Serial.printf("[Telemetry] HTTP POST failed, code: %d\n", httpCode);
    }
    http.end();

    // Re-enable promiscuous mode
    esp_wifi_set_promiscuous(true);
}

void setup() {
    Serial.begin(115200);
    WiFi.mode(WIFI_STA);
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\n[WiFi] Connected to network");

    // Configure Wi-Fi Promiscuous Mode
    esp_wifi_set_promiscuous_filter(NULL);
    esp_wifi_set_promiscuous_rx_cb(&promiscuous_rx_cb);
    esp_wifi_set_promiscuous(true);

    Serial.println("[RF Sniffer] Promiscuous mode enabled. Listening for packets...");
}

void loop() {
    delay(5000); // Flush and post telemetry every 5 seconds
    sendTelemetry();
}
