# Telegraf Role

This role deploys Telegraf via Nomad as a `system` job.

Telegraf is configured to scrape MQTT messages and system metrics across all nodes, pushing them directly to InfluxDB.
