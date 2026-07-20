# Connecting an Android Client to Headscale

This guide walks you through the process of connecting the official Tailscale Android client to our custom Headscale cluster mesh network.

## Prerequisites

* Your device must have network reachability to the Headscale service.
* You need to know your cluster domain. By default, this is `local.mesh`, making the Headscale URL `https://headscale.local.mesh`.

## 1. Installation

Install the official Tailscale Android client from your preferred app store:

* [Google Play Store](https://play.google.com/store/apps/details?id=com.tailscale.ipn)
* [F-Droid](https://f-droid.org/packages/com.tailscale.ipn/)

## 2. Connecting to the Node

You can authenticate the Android client using either web authentication or a pre-authenticated key.

### Option A: Connect via Web Authentication

1. Open the Tailscale app and select the **Settings menu** in the upper-right corner.
2. Tap on **Accounts**.
3. Tap the kebab menu icon (three dots) in the upper-right corner and select **Use an alternate server**.
4. Enter your Headscale server URL:
   * **URL:** `https://headscale.<your_cluster_domain>` (e.g., `https://headscale.local.mesh`)
5. Follow the on-screen instructions. The client will connect automatically as soon as the node registration is complete on the Headscale server. Until then, nothing is visible in the server logs.

### Option B: Connect using a Pre-Authenticated Key

1. Open the Tailscale app and select the **Settings menu** in the upper-right corner.
2. Tap on **Accounts**.
3. Tap the kebab menu icon (three dots) in the upper-right corner and select **Use an alternate server**.
4. Enter your Headscale server URL:
   * **URL:** `https://headscale.<your_cluster_domain>` (e.g., `https://headscale.local.mesh`)
5. If a login prompt opens, close it and continue.
6. Open the **Settings menu** again in the upper-right corner.
7. Tap on **Accounts**.
8. Tap the kebab menu icon (three dots) in the upper-right corner and select **Use an auth key**.
9. Enter your pre-auth key (see [Getting a Pre-Auth Key](#getting-a-pre-auth-key) below).
10. If needed, tap **Log in** on the main screen. You should now be connected to your Headscale mesh network.

## Getting a Pre-Auth Key

If you are an administrator, you need to provide users with a pre-authenticated key to use Option B.

### During Ansible Provisioning

The Ansible playbook automatically generates an initial 24-hour reusable pre-auth key for the default namespace during the cluster bootstrapping process. You can find this key by reviewing the output logs of the Ansible provisioning run, specifically during the `headscale` role execution under the task `Create pre-auth key` or `Set headscale auth key fact`.

### Generating Manually via CLI

If the initial key has expired or you need to generate a new one, log in to the node running Headscale and execute the following command:

```bash
headscale --user default preauthkeys create --reusable --expiration 24h
```

*(Note: Replace `default` with your specific namespace if you have customized the `headscale_namespace` variable in the Ansible configuration).*
