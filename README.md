# MiniZT — A Tiny Cloud-Based Virtual Network  
*Small enough to understand. Powerful enough to break. Free enough to fork without guilt.*

MiniZT is a compact, hackable virtual networking system that lets you spin up your own L2/L3 overlay network using three things:

- A microscopic Python Cloud Controller  
- A Linux auto-join client  
- A Windows auto-join client  

If ZeroTier had a tiny open-source baby and forgot to file the birth certificate, this would be it.

## 🎯 Who This Is For

- Students & hobbyists exploring overlay networks  
- Network engineers curious about how ZeroTier-like controllers actually work  
- Anyone needing a simple self-hosted virtual LAN/VPN for testing  
- People who enjoy breaking things, fixing them, breaking them again, then calling it “research”  

No license. No restrictions. No permissions.  
Fork it, sell it, burn it, rebuild it — **100% free forever.**

Inspired by ZeroTier, rewritten from scratch in a few tiny scripts.

---

# 🚀 Features

### ✔ Cloud Controller (Python)
A tiny API that:
- Generates a Network ID  
- Registers peers  
- Allocates IPs  
- Returns ready-made WireGuard configs  

### ✔ Linux Auto-Join Client (Bash)
- Generates keys  
- Calls the controller  
- Receives a config  
- Brings up a `wg0` interface  

### ✔ Windows Auto-Join Client (PowerShell, ≤20 lines)
A full working WG auto-join client that fits comfortably on a T-shirt.

### ✔ ZeroTier-like Experience
- Network ID  
- Auto-join  
- Auto IP assignment  
- WireGuard transport  
- Global L2/L3 virtual LAN  

---

# 🏗 Project Structure

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
