<div align="center">

<img src="icon.png" alt="Hawser Logo" width="200">

### Remote Docker agent for [Dockhand](https://dockhand.pro) - manage Docker hosts anywhere.

![Docker Pulls][docker-pulls-badge] ![Image Size][docker-size-badge] ![Docker Version][docker-version-badge] [![Docker Image][docker-image-badge]][docker-image-link]

[![GitHub Release][github-release-badge]][github-release-link] ![Workflow Status][github-workflow-badge] ![Github Issues][github-issues-badge] ![Github Last Commit][github-last-commit-badge]

[![Go Version](https://img.shields.io/github/go-mod/go-version/Finsys/hawser?logo=go&labelColor=31383f)](https://go.dev/)
[![License][github-license-badge]][license-link] ![Docker Stars][docker-stars-badge] ![Github Stars][github-stars-badge]

</div>

## [Overview](#top) 🚩

Hawser is a lightweight Go agent that enables Dockhand to manage Docker hosts in various network configurations. It supports two operational modes:

- **Standard Mode**: Agent listens for incoming connections (ideal for LAN/homelab with static IPs)
- **Edge Mode**: Agent initiates outbound WebSocket connection to Dockhand (ideal for VPS, NAT, dynamic IP)

[`^ Top`](#top)

## [Quick Start](#top) ⭐

> [!important]
> To install Hawser on a Server or VM, you really only need to following command:
> ```bash
> curl -fsSL https://raw.githubusercontent.com/Finsys/hawser/main/scripts/install.sh | bash
>```

### _Binary_

Download the latest release from [GitHub Releases](https://github.com/Finsys/hawser/releases).

#### Standard Mode

```bash
hawser --port 2376
```

#### Standard Mode with Token Auth (optional)

```bash
TOKEN=your-secret-token hawser --port 2376
```

#### Standard Mode with TLS (optional)

```bash
TLS_CERT=/path/to/server.crt TLS_KEY=/path/to/server.key hawser --port 2376
```

#### Standard Mode with TLS and Token Auth (for production)

```bash
TLS_CERT=/path/to/server.crt TLS_KEY=/path/to/server.key TOKEN=your-secret-token hawser --port 2376
```

#### Edge Mode

```bash
hawser --server wss://your-dockhand.example.com/api/hawser/connect --token your-token
```

#### Edge Mode with Self-Signed Certificate

```bash
CA_CERT=/path/to/dockhand-ca.crt hawser --server wss://your-dockhand.example.com/api/hawser/connect --token your-token
```

#### Edge Mode with TLS Skip Verify (insecure, for testing only)

```bash
TLS_SKIP_VERIFY=true hawser --server wss://your-dockhand.example.com/api/hawser/connect --token your-token
```

### _Systemd Service_

#### Quick Install

1. Download and install the binary:

```bash
curl -fsSL https://raw.githubusercontent.com/Finsys/hawser/main/scripts/install.sh | bash
```

2. Configure the service:

```bash
sudo nano /etc/hawser/config
```

Example config for **Standard Mode**:

```bash
# Standard mode - listen for connections
PORT=2376
# Optional: require token authentication
TOKEN=your-secret-token
```

Example config for **Edge Mode**:

```bash
# Edge mode - connect to Dockhand server
DOCKHAND_SERVER_URL=wss://your-dockhand.example.com/api/hawser/connect
TOKEN=your-agent-token
```

3. Start the service:

```bash
sudo systemctl enable --now hawser
```

#### Full Systemd Service File

If you prefer to set up the systemd service manually, here's the complete service file:

**`/etc/systemd/system/hawser.service`**

```ini
[Unit]
Description=Hawser - Remote Docker Agent for Dockhand
Documentation=https://github.com/Finsys/hawser
After=network-online.target docker.service
Wants=network-online.target
Requires=docker.service

[Service]
Type=simple
ExecStart=/usr/local/bin/hawser
Restart=always
RestartSec=10
EnvironmentFile=/etc/hawser/config

# Security hardening
NoNewPrivileges=false
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/run/docker.sock

[Install]
WantedBy=multi-user.target
```

**`/etc/hawser/config`** (Standard Mode example):

```bash
# Hawser Configuration
# See https://github.com/Finsys/hawser for documentation

# Standard Mode
PORT=2376

# Docker socket path
DOCKER_SOCKET=/var/run/docker.sock

# Agent identification (optional)
# AGENT_NAME=my-server

# Token authentication (optional)
# TOKEN=your-secret-token

# TLS configuration (optional)
# TLS_CERT=/etc/hawser/server.crt
# TLS_KEY=/etc/hawser/server.key
```

**`/etc/hawser/config`** (Edge Mode example):

```bash
# Hawser Configuration
# See https://github.com/Finsys/hawser for documentation

# Edge Mode - connect to Dockhand server
DOCKHAND_SERVER_URL=wss://your-dockhand.example.com/api/hawser/connect
TOKEN=your-agent-token

# Docker socket path
DOCKER_SOCKET=/var/run/docker.sock

# Agent identification (optional)
# AGENT_NAME=my-server

# TLS configuration for self-signed Dockhand (optional)
# CA_CERT=/etc/hawser/dockhand-ca.crt
# TLS_SKIP_VERIFY=false

# Connection settings (optional)
# HEARTBEAT_INTERVAL=30
# RECONNECT_DELAY=1
# MAX_RECONNECT_DELAY=60
```

### Manual Installation Steps

```bash
# 1. Download binary
curl -fsSL https://github.com/Finsys/hawser/releases/latest/download/hawser_linux_amd64.tar.gz | tar xz
sudo install -m 755 hawser /usr/local/bin/hawser

# 2. Create config directory
sudo mkdir -p /etc/hawser

# 3. Create config file (edit with your settings)
sudo tee /etc/hawser/config << 'EOF'
PORT=2376
DOCKER_SOCKET=/var/run/docker.sock
EOF

# 4. Create systemd service file
sudo tee /etc/systemd/system/hawser.service << 'EOF'
[Unit]
Description=Hawser - Remote Docker Agent for Dockhand
Documentation=https://github.com/Finsys/hawser
After=network-online.target docker.service
Wants=network-online.target
Requires=docker.service

[Service]
Type=simple
ExecStart=/usr/local/bin/hawser
Restart=always
RestartSec=10
EnvironmentFile=/etc/hawser/config

NoNewPrivileges=false
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/run/docker.sock

[Install]
WantedBy=multi-user.target
EOF

# 5. Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable --now hawser

# 6. Check status
sudo systemctl status hawser
sudo journalctl -u hawser -f
```

### Docker

#### Standard Mode - _Agent listens for connections:_

```bash
docker run -d \
  --name hawser \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -p 2376:2376 \
  ghcr.io/finsys/hawser:latest
```

#### Standard Mode with Token Auth (optional)

```bash
docker run -d \
  --name hawser \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -p 2376:2376 \
  -e TOKEN=your-secret-token \
  ghcr.io/finsys/hawser:latest
```

#### Standard Mode with TLS (optional)

```bash
docker run -d \
  --name hawser \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /path/to/certs:/certs:ro \
  -p 2376:2376 \
  -e TLS_CERT=/certs/server.crt \
  -e TLS_KEY=/certs/server.key \
  ghcr.io/finsys/hawser:latest
```

#### Standard Mode with TLS and Token Auth (for production)

```bash
docker run -d \
  --name hawser \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /path/to/certs:/certs:ro \
  -p 2376:2376 \
  -e TLS_CERT=/certs/server.crt \
  -e TLS_KEY=/certs/server.key \
  -e TOKEN=your-secret-token \
  ghcr.io/finsys/hawser:latest
```

#### Edge Mode - _Agent connects to Dockhand_

```bash
docker run -d \
  --name hawser \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e DOCKHAND_SERVER_URL=wss://your-dockhand.example.com/api/hawser/connect \
  -e TOKEN=your-agent-token \
  ghcr.io/finsys/hawser:latest
```

#### Edge Mode with Self-Signed Certificate

```bash
docker run -d \
  --name hawser \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /path/to/dockhand-ca.crt:/certs/ca.crt:ro \
  -e DOCKHAND_SERVER_URL=wss://your-dockhand.example.com/api/hawser/connect \
  -e TOKEN=your-agent-token \
  -e CA_CERT=/certs/ca.crt \
  ghcr.io/finsys/hawser:latest
```

### Docker health check

The Hawser Docker image includes a built-in health check that verifies Docker connectivity. This works in **both Standard and Edge modes**.

#### How it works:

- The container runs `wget` against the `/_hawser/health` endpoint every 30 seconds
- Both modes expose a minimal HTTP server on the configured port (default: 2376) for health checks
- The health check verifies that Hawser can communicate with the Docker daemon

#### Health check response:

```bash
# Standard mode
curl http://localhost:2376/_hawser/health
{"status":"healthy"}

# Edge mode (includes connection status)
curl http://localhost:2376/_hawser/health
{"status":"healthy","mode":"edge","connected":true}
```

#### Container Status


```bash
# Check container health status
docker inspect --format='{{.State.Health.Status}}' hawser
# healthy

# View health check logs
docker inspect --format='{{json .State.Health}}' hawser | jq
```

#### Custom health check (optional)

If you need custom health check settings, you can override the built-in health check:

```bash
docker run -d \
  --name hawser \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e DOCKHAND_SERVER_URL=wss://your-dockhand.example.com/api/hawser/connect \
  -e TOKEN=your-agent-token \
  --health-cmd="wget -q --spider http://localhost:2376/_hawser/health || exit 1" \
  --health-interval=30s \
  --health-timeout=5s \
  --health-retries=3 \
  --health-start-period=10s \
  ghcr.io/finsys/hawser:latest
```

[`^ Top`](#top)

## [Configuration](#top) 🚧

Hawser is configured via environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `DOCKHAND_SERVER_URL` | WebSocket URL for Edge mode | - |
| `TOKEN` | Authentication token | - |
| `CA_CERT` | Path to CA certificate for Edge mode (self-signed Dockhand) | - |
| `TLS_SKIP_VERIFY` | Skip TLS verification for Edge mode (insecure) | `false` |
| `PORT` | HTTP server port (Standard mode) | `2376` |
| `TLS_CERT` | Path to TLS certificate (Standard mode server cert) | - |
| `TLS_KEY` | Path to TLS private key (Standard mode server key) | - |
| `DOCKER_SOCKET` | Docker socket path | `/var/run/docker.sock` |
| `STACKS_DIR` | Directory for compose stack files (requires Dockhand 1.0.5+) | `/tmp/stacks` |
| `AGENT_ID` | Unique agent identifier | Auto-generated UUID |
| `AGENT_NAME` | Human-readable agent name | Hostname |
| `HEARTBEAT_INTERVAL` | Heartbeat interval in seconds | `30` |
| `REQUEST_TIMEOUT` | Request timeout in seconds | `30` |
| `RECONNECT_DELAY` | Initial reconnect delay (Edge mode) | `1` |
| `MAX_RECONNECT_DELAY` | Maximum reconnect delay | `60` |
| `LOG_LEVEL` | Logging level: `debug`, `info`, `warn`, `error` | `info` |

### Mode Detection

Hawser automatically detects the operational mode:

- If `DOCKHAND_SERVER_URL` and `TOKEN` are set → **Edge Mode**
- Otherwise → **Standard Mode**

### Log Levels

The `LOG_LEVEL` environment variable controls verbosity:

| Level | Description |
|-------|-------------|
| `debug` | All messages including Docker API calls (method, path, status codes) |
| `info` | Standard operational messages (connections, startup, shutdown) |
| `warn` | Warnings only |
| `error` | Errors only |

#### Example: Debug Mode

```bash
# Binary
LOG_LEVEL=debug hawser --port 2376

# Docker
docker run -d \
  --name hawser \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -p 2376:2376 \
  -e LOG_LEVEL=debug \
  ghcr.io/finsys/hawser:latest
```

Debug mode logs all Docker API requests, which is useful for troubleshooting connectivity issues.

[`^ Top`](#top)

## [Features](#top) ✨

### Docker API Proxy

Hawser provides full access to the Docker API:

- Container management (create, start, stop, remove)
- Image operations (pull, list, remove)
- Volume and network management
- Log streaming
- Interactive exec sessions

### Docker Compose Support

Hawser includes Docker Compose support for stack operations:

- `up` - Deploy stack
- `down` - Remove stack
- `pull` - Pull images
- `ps` - List services
- `logs` - View logs

### Host Metrics

Hawser collects and reports host metrics:

- CPU usage (per-core and total)
- Memory (total, used, available)
- Disk usage (Docker data directory)
- Network I/O statistics

Metrics are sent every 30 seconds in Edge mode.

### Reliability

- **Auto-reconnect**: Edge mode automatically reconnects with exponential backoff
- **Heartbeat**: Regular keepalive messages maintain connection health
- **Graceful shutdown**: Clean shutdown on SIGTERM/SIGINT

### Docker API Version Compatibility

Hawser automatically negotiates the Docker API version with the daemon. When running Docker Compose operations, Hawser sets the `DOCKER_API_VERSION` environment variable to match the daemon's reported API version. This ensures compatibility when the Docker CLI version differs from the daemon version - for example, when using an older Docker CLI with a newer Docker daemon that requires a higher minimum API version.

[`^ Top`](#top)

## [API Endpoints](#top) 📁

### Standard Mode

In Standard mode, Hawser proxies all Docker API endpoints plus:

| Endpoint | Description |
|----------|-------------|
| `/_hawser/health` | Health check (no auth required) |
| `/_hawser/info` | Agent information |

### Health Check

```bash
# Standard mode
curl http://localhost:2376/_hawser/health
# {"status":"healthy"}

# Edge mode (includes WebSocket connection status)
curl http://localhost:2376/_hawser/health
# {"status":"healthy","mode":"edge","connected":true}
```

[`^ Top`](#top)

## [Security Considerations](#top) 🔒

1. **Docker Socket Access**: Hawser requires access to the Docker socket, which provides full control over Docker. Run with appropriate access controls.

2. **Network Security**:
	- Standard mode: Use TLS and/or token authentication
	- Edge mode: Use WSS (TLS-encrypted WebSocket)

3. **Token Security**: Tokens should be strong, randomly generated strings. In Dockhand, tokens are shown only once when generated.

[`^ Top`](#top)

## [Resources](#top) 📖

- [Dockhand](https://dockhand.pro) - Modern Docker management application
- [Docker Engine API](https://docs.docker.com/engine/api/) - Docker API documentation

[`^ Top`](#top)

## [License](#top) ⚖️

[![][github-license-badge]][license-link]

[`^ Top`](#top)




[docker-pulls-badge]: https://img.shields.io/docker/pulls/fnsys/dockhand?labelColor=31383f&logo=docker
[docker-size-badge]: https://img.shields.io/docker/image-size/fnsys/dockhand?labelColor=31383f&logo=docker
[docker-stars-badge]: https://img.shields.io/docker/stars/fnsys/dockhand?style=social
[docker-version-badge]: https://img.shields.io/docker/v/fnsys/dockhand?labelColor=31383f&logo=docker
[docker-image-badge]: https://img.shields.io/badge/docker-ghcr.io%2Ffinsys%2Fhawser-blue?labelColor=31383f&logo=docker

[github-issues-badge]: https://img.shields.io/github/issues/finsys/hawser?labelColor=31383f&logo=github
[github-last-commit-badge]: https://img.shields.io/github/last-commit/finsys/hawser?labelColor=31383f
[github-stars-badge]: https://img.shields.io/github/stars/finsys/hawser
[github-license-badge]: https://img.shields.io/badge/License-MIT-yellow?color=ffff00&labelColor=31383f
[github-release-badge]: https://img.shields.io/github/release/Finsys/hawser?labelColor=31383f&logo=github
[github-workflow-badge]: https://img.shields.io/github/actions/workflow/status/Finsys/hawser/build.yml?branch=main&labelColor=31383f&logo=github&label=build

[license-link]: https://choosealicense.com/licenses/mit/
[docker-image-link]: https://github.com/Finsys/hawser/pkgs/container/hawser
[github-release-link]: https://github.com/Finsys/hawser/actions/workflows/release.yml