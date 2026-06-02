# Zigbee2MQTT Role

This role deploys Zigbee2MQTT via Nomad, configured to connect to the local MQTT broker and bridge Zigbee devices without needing a heavy UI like Home Assistant.

It expects `meta.zigbee_coordinator = "true"` on the Nomad client where the USB dongle is connected, and mounts the device directly via privileged docker mode. You can configure the port using `zigbee2mqtt_port` and the serial device using `zigbee_serial_port`.
