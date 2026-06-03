# AI Coding Agents Guide for .labware

## Project Overview
.labware is a Python CLI tool for homelab self-hosting, providing Docker Compose templates for services (in `svc/`) and installation/setup orchestration for servers (in `scr/`). The core is a typer-based CLI in `src/labware/`.

## Architecture
- **CLI Entry**: `src/labware/cli.py` - Typer app (entrypoint `lab` in `pyproject.toml`) with commands like `setup` and `version`. The CLI imports and delegates setup to `scr.setup.setup` (see `src/labware/cli.py`).
- **Installation / Setup**: `scr/setup/setup.py` - Primary setup orchestrator (invoked by `lab setup`) that runs system checks (root, Ubuntu), enforces the project's Python requirement (see `pyproject.toml`), and runs a large set of hardening/install steps implemented as `scr/setup/sec/*` modules (examples: `sec.users`, `sec.tools`, `sec.firewalld`).
- **Config**: `src/labware/config.py` - Provides `DEFAULT_CONFIG` in-code and a `Config`/`get_config()` singleton. External config files are optional; the repository ships a canonical config at `scr/lab/cfg/.labware.cfg` and many runtime modules construct the Config with that file (e.g., `BASEDIR / "scr" / "lab" / "cfg" / ".labware.cfg"`). Use `config.get(...)`, `config.getint(...)`, `config.getbool(...)` to access values; the loader will also search common locations (e.g., `~/.labware.cfg`, `~/.labware/.labware.cfg`, `/usr/share/labware/.labware.cfg`) when no explicit path is supplied.
- **Services**: `svc/` - Each service subdir (e.g., `svc/ackee/`) follows a `docker-compose.yml` + `logo.png` pattern and acts as a deployment template for that service.
- **Scripts**: `scr/` - Contains `scr/setup/` (Python orchestrator & `sec/` modules), `scr/lab/` (config stubs), and `scr/pkg/` (packaging/install helpers). Some legacy bash installers may still exist under `scr/pkg` or `scr/lab`, but the primary installation flow is Python-driven.

Data flows from CLI to config/logger/output/filesys and then to `scr/setup/sec/*` modules which perform system operations and subprocess calls via a single `run()` helper.

## Key Workflows
- **Setup Tool**: Run `lab setup` (entrypoint `lab`, requires root). This invokes `scr/setup/setup.py` which:
  - checks environment (root, OS, Python runtime),
  - installs users/tools, packages and templates,
  - applies CIS-style hardening via many `scr/setup/sec/*` modules,
  - writes files/templates (Jinja2) and may prompt for confirmation, and
  - optionally reboots the system at the end.
- **Deploy Service**: Use `docker-compose up` in `svc/{service}/` (e.g., `svc/ackee/docker-compose.yml`).
- **Install External Tools**: Some package installers live under `scr/pkg/` and may download releases from GitHub; the main setup flow uses the Python `scr/setup` modules.
- **Debug**: Check logs in the configured log directory (default `~/.labware/log`) — logging is configured via `src/labware/logger.py`.

## Conventions
- **CLI**: Use Typer with `rich_markup_mode="rich"` and rich-based help; the CLI exposes commands (e.g., `setup`, `version`) and delegates heavy work to modules under `scr/setup/`.
- **Paths**: Use `pathlib.Path` and a computed `BASEDIR` (e.g., `BASEDIR = Path(__file__).parents[2]`) to locate repo resources.
- **Commands**: Use the centralized `run()` helper in `src/labware/utils.py` for shell/subprocess execution; it logs commands and returns `subprocess.CompletedProcess` (supports `capture=True`, `check=False`).
- **Output**: Console helpers live in `src/labware/output.py` (e.g., `printSuccess()`, `printError()`, `printHead()`, `getData()`), backed by `rich` and by styles defined in config.
- **Config Access**: Import the singleton `config` from `labware.config` and call `config.get("section", "option")` or `config.getint(...)`/`getbool(...)`. Example: `config.get("src", "setup")` (see `scr/setup/setup.py`).
- **Imports**: Code generally imports via the package namespace (e.g., `from labware.config import *`) and some modules append `BASEDIR` to `sys.path` to import `scr` helpers (this is the current pattern used by the CLI and setup modules).

## Patterns
- **Service Templates**: Each `svc/` directory contains a `docker-compose.yml` and auxiliary assets (icons, README). When contributing a new service, match the existing directory layout (example: `svc/ackee/`).
- **Setup Modules**: The setup flow is split into many focused modules under `scr/setup/sec/` (users, tools, network, firewalld, sshd, sudo, auditd, etc.). Each `sec.*.py` exposes an `execute()` entry used by `scr/setup/setup.py`.
- **Templating**: Configuration files and unit templates are rendered with Jinja2 via `src/labware/filesys.py` (`loader = Environment(FileSystemLoader(config.get("paths", "templates")))`). Templates are placed under `scr/setup/etc` by default (see `scr/lab/cfg/.labware.cfg`).
- **File operations & permissions**: `src/labware/filesys.py` provides helpers (`copyFiles`, `writeTemplate`, `chmod`, `chown`) which all log via the project logger and use `pathlib.Path`.
- **Error Handling**: The project uses a custom `Logger` (`src/labware/logger.py`) which provides convenience methods (`error()`, `info()`, `debug()`, `outlog()`); fatal errors are typically surfaced via `logger.error(..., True)` and the `run()` helper may call `sys.exit(1)` when `check=True`.
- **User Prompts**: Interactive prompts and pauses use `output.getData()` so agents should avoid driving interactive flows unless explicitly requested.

## External Integrations
- **Docker**: Compose files assume Docker installed; services reference images from registries (Docker Hub or other configured registries).
- **GitHub API / Releases**: Some installers in `scr/pkg/` query GitHub releases to obtain the latest binaries.
- **Templating & Packaging**: `jinja2` is used for configuration templating and `pyproject.toml` defines packaging/entry points (see `[project.scripts] lab = "labware.cli:app"`).
- **System**: The setup flow relies on standard Linux utilities: `sudo`, `apt`, `systemctl`, `lsb_release`, user/group utilities, and systemd behaviors.

Reference: `pyproject.toml` for deps (typer, rich, sqlitedict, jinja2), `src/labware/__init__.py` for version.
