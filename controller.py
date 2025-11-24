#!/usr/bin/env python3
# MiniZT - Minimal ZeroTier-like Controller (Free & Unrestricted)
# Run:  python3 controller.py

from flask import Flask, request, jsonify
import secrets

app = Flask(__name__)

# ---- NETWORK SETTINGS ----
NETWORK_ID = secrets.token_hex(4)       # random 8-char network ID
NETWORK_CIDR = "10.1.1.0/24"
GATEWAY_IP = "10.1.1.1"

# Load your WireGuard server public key
with open("server.pub", "r") as f:
    SERVER_PUBLIC_KEY = f.read().strip()

SERVER_ENDPOINT = "1.2.3.4:51820"  # <-- replace with your server public IP:port

# In-memory peer store
peers = {}  # pubkey -> assigned IP


def next_ip():
    used_ids = [int(ip.split(".")[-1]) for ip in peers.values()]
    host_id = 2
    while host_id in used_ids:
        host_id += 1
    return f"10.1.1.{host_id}"


@app.route("/join", methods=["POST"])
def join():
    pubkey = request.json.get("pubkey")
    if not pubkey:
        return jsonify({"error": "Missing pubkey"}), 400

    if pubkey not in peers:
        peers[pubkey] = next_ip()

    assigned_ip = peers[pubkey]

    config_template = f"""
[Interface]
Address = {assigned_ip}/24
PrivateKey = <client_private_key>
DNS = 1.1.1.1

[Peer]
PublicKey = {SERVER_PUBLIC_KEY}
Endpoint = {SERVER_ENDPOINT}
AllowedIPs = {NETWORK_CIDR}
PersistentKeepalive = 25
"""

    return jsonify({
        "network_id": NETWORK_ID,
        "assigned_ip": assigned_ip,
        "wg_config_template": config_template
    })


@app.route("/info")
def info():
    return jsonify({"network_id": NETWORK_ID, "peers": peers})


if __name__ == "__main__":
    print(f"MiniZT Controller running. Network ID: {NETWORK_ID}")
    app.run("0.0.0.0", 8080)
