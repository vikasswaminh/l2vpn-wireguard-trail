write it as beautiful markdown for my github as personal as possible with little humour and intelligence combined MiniZT — A Tiny Cloud-Based Virtual Network (Free, Open, Modifiable)

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

i know what you are thinking, yes we will do doing all that, 
Alternative High-Performance Methods for L2/L3 Overlays on Linux
1. Kernel VXLAN (native)

Hardware-offload friendly (NICs with VXLAN offload).

Lower overhead than user-space solutions.

Ideal for large multi-node L2 fabrics.

2. Geneve (successor to VXLAN)

Extensible TLV metadata.

Better integration with SDN controllers (OVN, OpenStack).

Increasing hardware offload support.

3. GRETAP / FOU (Foo-over-UDP)

Simple L2 tunneling with low overhead.

GRETAP+FOU reduces GRE performance penalties.

Suitable for site-to-site bridging or lab networks.

4. L2TPv3 (Ethernet pseudowire)

True point-to-point L2 circuits.

Good for service-provider-style transparent Ethernet transport.

Light and reliable, but not multi-point like VXLAN.

5. EVPN + VXLAN (FRR + Linux)

Enterprise-grade distributed L2 and L3 fabric.

Uses BGP EVPN control plane.

Scales to thousands of endpoints with MAC/IP route distribution.

6. eBPF/XDP Accelerated Overlays

Custom encapsulation in eBPF for ultra-low latency.

Can outperform VXLAN in CPU-bound scenarios.

Requires BPF programming but extremely fast.

curl/jq for Linux client

/controller.py → Cloud controller & Network ID generator
/linux-join.sh → Linux auto-join client
/win-join.ps1 → Windows auto-join client
/server.pub → WireGuard server public key


---

# 🌐 High-Level Architecture

1. You run `controller.py` on a public server  
2. Clients generate their WireGuard keys locally  
3. They POST their public key to the controller  
4. Controller assigns an IP (10.1.1.x)  
5. Controller returns a fully-baked WireGuard config  
6. Client inserts its private key  
7. Tunnel comes online  

Congratulations — every device now lives on the same virtual LAN.  
ZeroTier/Headscale/Tailscale vibes, pocket-sized.

---

# 📡 1. Cloud Controller (Python)

Run your controller:

```bash
pip install flask
python3 controller.py


It automatically creates:

Network ID

Peer IP allocator

WireGuard template

No database. No storage.
Everything in RAM. If you reboot your server, the peers disappear like your weekend productivity.

🐧 2. Linux Auto-Join Script
./linux-join.sh


What it does:

Generates WG keys

Calls the controller

Receives config

Injects private key

Brings up wg0

Your machine appears as:

10.1.1.X

🪟 3. Windows Auto-Join Client (≤20 Lines)

Below is the complete PowerShell WireGuard client:

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

Usage
powershell -ExecutionPolicy Bypass -File wg-client.ps1 -ServerIP 45.12.22.10 -HostID 5


Your Windows node becomes:

10.1.1.5

🛠 Requirements

A Linux server with a public IP

WireGuard installed everywhere

Flask on controller

curl + jq for Linux

WireGuard.exe for Windows

🌀 Alternative High-Performance Overlays (For the Curious)

Sometimes you want tiny scripts.
Sometimes you want “my laptop is now a data center switch.”

Here are the big guns:

1. VXLAN (Kernel)

Hardware-offload friendly

Low overhead

Great for multi-node L2 fabrics

2. Geneve

VXLAN’s smarter cousin

Better metadata TLV support

Integrates with OVN / OpenStack

3. GRETAP + FOU

Simple L2 tunneling

FOU reduces GRE overhead

Ideal for lab topologies

4. L2TPv3

True point-to-point Ethernet pseudowires

Lightweight and stable

5. EVPN + VXLAN (FRR + Linux)

Full enterprise fabric

BGP EVPN control plane

Thousands of endpoints

6. eBPF/XDP Overlays

Custom encapsulation

Ultra-low latency

Very fast, very fun, slightly dangerous

🧪 Why This Exists

I am building these systems for my research organization:
https://www.namahos.com

And yes — we will be doing all of that.

If you plan on using MiniZT in your own experiments, forks, research projects, or spontaneous weekend chaos engineering, enjoy.

MiniZT is intentionally tiny so you can understand every moving part — then replace it with something cooler.

⭐ If You Use This, Consider…

WireGuard.exe for Windows client

Building these products for my research company https://www.namahos.com
