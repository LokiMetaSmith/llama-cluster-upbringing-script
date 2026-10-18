/**
 * ESP32 Reference Implementation for Proximity Challenge/Response
 *
 * This Arduino sketch demonstrates an ESP32 acting as an intermediate room
 * reader or a smart badge. It uses standard HTTP libraries to fetch a challenge
 * and mbedtls for ECDSA P-256 (SECP256R1) signing.
 *
 * Dependencies:
 * - ArduinoJSON (for deterministic payload generation)
 * - HTTPClient / WiFi
 * - mbedtls (built into ESP32 core)
 */

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "mbedtls/ecdsa.h"
#include "mbedtls/sha256.h"
#include "mbedtls/entropy.h"
#include "mbedtls/ctr_drbg.h"
#include "mbedtls/base64.h"

const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";

const char* DAEMON_URL_CHALLENGE = "http://192.168.1.100:8011/api/v1/challenge?room_id=room_101";
const char* DAEMON_URL_VERIFY = "http://192.168.1.100:8011/api/v1/verify";
const char* ROOM_ID = "room_101";
const char* DID = "did:example:esp32-node-001";
const char* SECRET_HEADER = "secret"; // Matches TAP_ORCHESTRATOR_SECRET

// Global cryptographic contexts
mbedtls_ecdsa_context ecdsa_ctx;
mbedtls_entropy_context entropy;
mbedtls_ctr_drbg_context ctr_drbg;
char pub_key_hex[130]; // 65 bytes * 2 (hex) + null terminator

void initCrypto() {
    mbedtls_ecdsa_init(&ecdsa_ctx);
    mbedtls_entropy_init(&entropy);
    mbedtls_ctr_drbg_init(&ctr_drbg);

    const char* seed = "esp32_random_seed";
    mbedtls_ctr_drbg_seed(&ctr_drbg, mbedtls_entropy_func, &entropy, (const unsigned char *)seed, strlen(seed));

    // Generate SECP256R1 keypair
    mbedtls_ecdsa_genkey(&ecdsa_ctx, MBEDTLS_ECP_DP_SECP256R1, mbedtls_ctr_drbg_random, &ctr_drbg);

    // Extract public key to hex (Uncompressed format starts with 0x04)
    unsigned char pub_bytes[65];
    size_t olen;
    mbedtls_ecp_point_write_binary(&ecdsa_ctx.grp, &ecdsa_ctx.Q, MBEDTLS_ECP_PF_UNCOMPRESSED, &olen, pub_bytes, sizeof(pub_bytes));

    for (int i = 0; i < 65; i++) {
        sprintf(&pub_key_hex[i*2], "%02x", pub_bytes[i]);
    }
    Serial.printf("Generated Public Key: %s\n", pub_key_hex);
}

String fetchChallenge() {
    HTTPClient http;
    http.begin(DAEMON_URL_CHALLENGE);
    http.addHeader("X-Tap-Secret", SECRET_HEADER);

    int httpResponseCode = http.GET();
    String nonce = "";

    if (httpResponseCode == 200) {
        String payload = http.getString();
        StaticJsonDocument<200> doc;
        deserializeJson(doc, payload);
        nonce = doc["nonce"].as<String>();
        Serial.printf("Received nonce: %s\n", nonce.c_str());
    } else {
        Serial.printf("Error fetching challenge: %d\n", httpResponseCode);
    }
    http.end();
    return nonce;
}

String signPayload(String nonce, String room) {
    // 1. Create Deterministic JSON (Keys sorted alphabetically)
    // {"challenge_nonce":"<nonce>","room_id":"<room>"}
    String jsonPayload = "{\"challenge_nonce\":\"" + nonce + "\",\"room_id\":\"" + room + "\"}";

    // 2. Hash the payload with SHA-256
    unsigned char hash[32];
    mbedtls_sha256_ret((const unsigned char*)jsonPayload.c_str(), jsonPayload.length(), hash, 0);

    // 3. Sign the hash
    mbedtls_mpi r, s;
    mbedtls_mpi_init(&r);
    mbedtls_mpi_init(&s);

    mbedtls_ecdsa_sign(&ecdsa_ctx.grp, &r, &s, &ecdsa_ctx.d, hash, 32, mbedtls_ctr_drbg_random, &ctr_drbg);

    // 4. Serialize signature to DER format
    unsigned char sig_der[72];
    unsigned char *p = sig_der + sizeof(sig_der);
    size_t sig_len = 0;

    mbedtls_asn1_write_mpi(&p, sig_der, &s);
    mbedtls_asn1_write_mpi(&p, sig_der, &r);
    sig_len = (sig_der + sizeof(sig_der)) - p;

    unsigned char final_der[72];
    unsigned char *p2 = final_der + sizeof(final_der);
    mbedtls_asn1_write_len(&p2, final_der, sig_len);
    mbedtls_asn1_write_tag(&p2, final_der, MBEDTLS_ASN1_CONSTRUCTED | MBEDTLS_ASN1_SEQUENCE);
    size_t final_len = (final_der + sizeof(final_der)) - p2;

    // 5. Base64 encode the DER signature
    unsigned char b64_sig[128];
    size_t b64_len;
    mbedtls_base64_encode(b64_sig, sizeof(b64_sig), &b64_len, p2, final_len);

    mbedtls_mpi_free(&r);
    mbedtls_mpi_free(&s);

    return String((char*)b64_sig);
}

void verifyPresence(String nonce, String signature) {
    HTTPClient http;
    http.begin(DAEMON_URL_VERIFY);
    http.addHeader("Content-Type", "application/json");
    http.addHeader("X-Tap-Secret", SECRET_HEADER);

    StaticJsonDocument<512> doc;
    doc["did"] = DID;
    doc["challenge_nonce"] = nonce;
    doc["signature"] = signature;
    doc["room_id"] = ROOM_ID;
    doc["public_key_hex"] = pub_key_hex;

    String requestBody;
    serializeJson(doc, requestBody);

    int httpResponseCode = http.POST(requestBody);
    if (httpResponseCode == 200) {
        String response = http.getString();
        Serial.println("Presence Verified Successfully!");
        Serial.println(response);
    } else {
        Serial.printf("Verification Failed: %d\n", httpResponseCode);
        Serial.println(http.getString());
    }
    http.end();
}

void setup() {
    Serial.begin(115200);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }
    Serial.println("Connected to WiFi");

    initCrypto();

    String nonce = fetchChallenge();
    if (nonce != "") {
        String signature = signPayload(nonce, String(ROOM_ID));
        Serial.printf("Signature: %s\n", signature.c_str());
        verifyPresence(nonce, signature);
    }
}

void loop() {
    // Only running once in setup for demonstration
    delay(10000);
}
