# AI Coding Agents Guide for .labware

## Project Overview
.labware is a Python CLI tool for homelab self-hosting, providing Docker Compose templates for services (in `svc/`) and installation scripts for tools (in `scr/`). The core is a typer-based CLI in `src/labware/`.

## Architecture
- **CLI Entry**: `src/labware/cli.py` - Typer app with subcommands like `install`, `env`, `version`.
- **Installation**: `src/labware/install.py` - System checks (root, Ubuntu 24.04, Python 3.12+), file copying.
- **Config**: `src/labware/config.py` - Loads from `src/labware/config/.default.cfg` and `~/.labware.cfg` using ConfigParser.
- **Services**: `svc/` - Each subdir (e.g., `ackee/`) contains `docker-compose.yml` and `logo.png` for deployment.
- **Scripts**: `scr/` - Bash installers for external tools like Hawser, LazyDocker.

Data flows from CLI to config/logging/console, with subprocess calls for system interactions.

## Key Workflows
- **Install Tool**: Run `lab install` (requires root); checks system, copies files to `~/.labware/`.
- **Deploy Service**: Use `docker-compose up` in `svc/{service}/` (e.g., `svc/ackee/docker-compose.yml`).
- **Install External Tools**: Execute scripts like `scr/hawser_install.sh` (downloads binaries from GitHub releases).
- **Debug**: Check logs in `~/.labware/log/` (configured in config).

## Conventions
- **CLI**: Use typer with `rich_markup_mode="rich"`, options in panels (e.g., `rich_help_panel="Output Panel"`).
- **Paths**: Use `pathlib.Path` (e.g., `SCR_PATH = Path(__file__).resolve()`).
- **Commands**: Wrap subprocess in `run()` function with error handling (e.g., `run("lsb_release -rs", capture=True)`).
- **Output**: Custom console functions like `printSuccess()`, `printError()` from `console.py`.
- **Config Access**: `config.get("dirs", "dot")` for sections/keys.
- **Imports**: Relative imports (e.g., `from .console import *`).

## Patterns
- **Service Templates**: Each `svc/` dir follows `docker-compose.yml` + `logo.png` structure.
- **Script Installers**: Detect OS/arch, fetch latest release from GitHub API, extract tar.gz.
- **Error Handling**: `errorExit()` for fatal errors, logging with custom levels.
- **User Prompts**: Interactive input for usernames (e.g., in `install.py`).

## External Integrations
- **Docker**: Compose files assume Docker installed; services use images from Docker Hub.
- **GitHub API**: Scripts query releases for version detection.
- **System**: Relies on `sudo`, `lsb_release`, user management.

Reference: `pyproject.toml` for deps (typer, sqlitedict, jinja2), `src/labware/__init__.py` for version.</content>
<parameter name="filePath">\\wsl.localhost\Ubuntu\home\ragdata\projects\ragdata\.labware\AGENTS.md
