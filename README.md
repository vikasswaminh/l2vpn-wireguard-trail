MiniZT — A Tiny Cloud-Based Virtual Network (Free, Open, Modifiable)

MiniZT is a miniature, hackable,  virtual networking system that lets you create your own L2/L3 overlay network using WireGuard, a Cloud Controller, and auto-join Linux/Windows clients.

This project is meant for:

Students & hobbyists exploring overlay networks

Network engineers who want to understand ZeroTier-like architectures

People who want a simple self-hosted virtual LAN/VPN for testing

Anyone who wants to hack, fork, break, or rebuild everything freely

There is no license, no restrictions, no permissions required.
Do whatever you want with the code. Fork it, sell it, delete it, improve it — 100% free forever.

This project is inspired by ZeroTier, but rewritten from scratch in three tiny scripts.

🚀 What This Project Provides
✔ A Cloud Controller

A tiny Python API that generates a Network ID, registers peers, assigns IPs, and returns auto-generated WireGuard configs.

✔ Linux Auto-Join Client

A Bash script that generates keys, calls the controller, receives config, and starts WireGuard.

✔ Windows Auto-Join Client

A PowerShell client (≤20 lines) that automatically joins the network and brings up a WireGuard interface.

✔ A ZeroTier-like Experience

Network ID

Auto-join

Auto IP assignment

WireGuard transport

“Client appears inside same subnet on all machines”

Works anywhere on the Internet

🏗 Project Structure
/controller.py        → Cloud controller & network ID generator
/linux-join.sh        → Linux auto-join client
/win-join.ps1         → Windows auto-join client
/server.pub           → Server public key (generated during setup)

🌐 How It All Works – High Level

You run the controller on a public server.

Clients (Linux/Windows) generate WireGuard keys locally.

They send their public key to the controller.

Controller assigns an IP (10.1.1.x) and returns a ready-made WG config.

Client injects its private key into the template.

Tunnel comes up → all devices appear on the same virtual LAN.

This is exactly how ZeroTier/Headscale/Tailscale-style network controllers work — but rewritten to fit in your pocket.

📡 1. Cloud Controller (Python)

Create a cloud controller using:

controller.py


This exposes two API routes:

POST /join → register peer + return config

GET /info → view network status

Run:

pip install flask
python3 controller.py


It will automatically generate:

a Network ID

a peer IP allocator

a WireGuard config template

No database. No storage. Everything in RAM for simplicity.

🐧 2. Linux Auto-Join Script

Run on any Linux machine:

./linux-join.sh


It will:

Generate keys

Call controller

Receive config template

Insert private key

Bring up wg0

Machine is now reachable at:
10.1.1.X (assigned by controller)

🪟 3. Windows Auto-Join Script (PowerShell)

Below is the full 20-line Windows client that you can include in your repo.

⚡ wg-client.ps1 — Windows WireGuard Client (≤20 Lines)
# Windows WireGuard Client - 20 lines
param(
    [string]$ServerIP = "1.2.3.4",
    [int]$HostID = 2,
    [string]$ServerPubKey = "PUT_SERVER_PUBLIC_KEY_HERE"
)

$wgPath = "$env:ProgramFiles\WireGuard\wireguard.exe"
$keyDir = "$env:USERPROFILE\AppData\Local\wgkeys"
$newPriv = "$keyDir\client.key"
mkdir $keyDir -ErrorAction SilentlyContinue | Out-Null

# Generate client private key if not exists
if (!(Test-Path $newPriv)) {
    wg genkey | Out-File $newPriv
}
$priv = Get-Content $newPriv
$pub = wg pubkey | Out-String

# Build config
$config = @"
[Interface]
Address = 10.1.1.$HostID/24
PrivateKey = $priv
DNS = 1.1.1.1

[Peer]
PublicKey = $ServerPubKey
Endpoint = $ServerIP:51820
AllowedIPs = 10.1.1.0/24
PersistentKeepalive = 25
"@

# Write config file
$confPath = "$env:USERPROFILE\wg0.conf"
$config | Out-File $confPath -Encoding ascii

# Import + activate
& $wgPath /installtunnelservice $confPath
Start-Sleep -Seconds 2
& $wgPath /up wg0.conf

Write-Host "WireGuard client up. IP = 10.1.1.$HostID"

🧠 How to Use the Windows Client

Install WireGuard for Windows

Save the script as:

wg-client.ps1


Edit your server’s public key:

$ServerPubKey = "PUT_SERVER_PUBLIC_KEY_HERE"


Run:

powershell -ExecutionPolicy Bypass -File wg-client.ps1 -ServerIP 45.12.22.10 -HostID 5


Your Windows machine will now join the overlay network as:

10.1.1.5

Requirements

A Linux server with a public IP

WireGuard installed on server & clients

Flask (for controller)

curl/jq for Linux client

WireGuard.exe for Windows client
