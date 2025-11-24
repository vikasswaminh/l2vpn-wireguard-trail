#!/bin/bash
# MiniZT - Linux Auto Join Client (Free & Unrestricted)

CTRL="http://1.2.3.4:8080"   # <-- controller address
mkdir -p /etc/wg-mini

# Generate keys if missing
if [ ! -f /etc/wg-mini/priv ]; then
    echo "Generating keys..."
    wg genkey | tee /etc/wg-mini/priv | wg pubkey >/etc/wg-mini/pub
fi

PUB=$(cat /etc/wg-mini/pub)

# Join the network
RESP=$(curl -s -X POST -H "Content-Type: application/json" \
    -d "{\"pubkey\":\"$PUB\"}" $CTRL/join)

if [ -z "$RESP" ]; then
    echo "Error: No response from controller."
    exit 1
fi

IP=$(echo "$RESP" | jq -r .assigned_ip)
CFG=$(echo "$RESP" | jq -r .wg_config_template)

# Insert private key
echo "$CFG" | sed "s#<client_private_key>#$(cat /etc/wg-mini/priv)#" \
    >/etc/wireguard/wg0.conf

# Bring interface up
wg-quick down wg0 2>/dev/null
wg-quick up wg0

echo "Joined MiniZT network successfully!"
echo "Assigned IP: $IP"
