#!/usr/bin/env bash
# shellcheck disable=SC2004
# shellcheck disable=SC2034
# shellcheck disable=SC2016
# shellcheck disable=SC1090
####################################################################
# install.sh
####################################################################
# File:         install.sh
# Author:       Ragdata
# Date:         12/04/2026
# License:      MIT License
# Repository:	https://github.com/Ragdata/.dotfiles
# Copyright:    Copyright © 2026 Redeyed Technologies
####################################################################
# PRE-FLIGHT
####################################################################
# set -x

# LOCAL VARIABLES
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

. vendor/progressbar
####################################################################
# FUNCTIONS
####################################################################
print::message() {
	local color="${2:-$GREEN}"
	echo -e "${color}${1}${NC}"
}

print::error() { print::message "[ERROR]: ${1}" "$RED"; }

print::warn() { print::message "[WARNING]: ${1}" "$YELLOW"; }

print::info() { print::message "[INFO: ${1}" "$BLUE"; }

print::success() { print::message "[SUCCESS]: ${1}" "$GREEN"; }

print::head() { print::message "${1}" "$YELLOW"; }

print::default() { print::message "${1}"; }

error::exit() {
	print::error "$1"
	exit 1
}

install::files() {
    local src="$1" dst="$2"

    for item in "$src"/*; do
        if [ -d "$item" ]; then
            mkdir -p "$dst/$(basename "$item")"
            install::files "$item" "$dst/$(basename "$item")"
        else
            if ! install -m 644 "$item" "$dst/$(basename "$item")"; then
                print::warn "Failed to install '$item'"
            fi
        fi
    done
}
####################################################################
# VARIABLES
####################################################################
# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# TOOLS
tools=("make"
	"build-essential"
	"libssl-dev"
	"zlib1g-dev"
	"libbz2-dev"
	"libreadline-dev"
	"libsqlite3-dev"
	"curl"
	"wget"
	"git"
	"libncursesw5-dev"
	"xz-utils"
	"tk-dev"
	"libxml2-dev"
	"libxmlsec1-dev"
	"libffi-dev"
	"liblzma-dev")

dirs=(".backup"
	".bashrc.d/prompts"
	".labware/lib/aliases"
	".labware/lib/completions"
	".labware/lib/functions"
	".labware/log"
	".labware/reg")

# OPERATING VARIABLES
DEBIAN_FRONTEND=noninteractive

# Detect the actual user for pyenv operations
# This script is designed to run as root, but pyenv should be for the regular user
if [ -n "$SUDO_USER" ] && [ "$SUDO_USER" != "root" ]; then
    # Run with sudo from regular user
    ACTUAL_USER="$SUDO_USER"
    ACTUAL_HOME=$(eval echo "~$SUDO_USER")
    print::info "Detected sudo user: $ACTUAL_USER (home: $ACTUAL_HOME)"
elif [ "$USER" = "root" ]; then
    # Running as root - find the appropriate user for pyenv
    # Check if there's a SUDO_USER set from a previous sudo
    if [ -n "$SUDO_USER" ]; then
        ACTUAL_USER="$SUDO_USER"
        ACTUAL_HOME=$(eval echo "~$SUDO_USER")
        print::info "Using previous sudo user: $ACTUAL_USER (home: $ACTUAL_HOME)"
    else
        # No sudo user - check script owner or common users
        SCRIPT_OWNER=$(stat -c '%U' "$SCRIPT_DIR")
        if [ "$SCRIPT_OWNER" != "root" ]; then
            ACTUAL_USER="$SCRIPT_OWNER"
            ACTUAL_HOME=$(eval echo "~$SCRIPT_OWNER")
            print::info "Using script owner: $ACTUAL_USER (home: $ACTUAL_HOME)"
        else
            # Fallback: look for existing pyenv installation
            for potential_user in "ragdata" "$(whoami 2>/dev/null | head -1)" "$(logname 2>/dev/null)"; do
                if [ -d "/home/$potential_user/.pyenv" ]; then
                    ACTUAL_USER="$potential_user"
                    ACTUAL_HOME="/home/$potential_user"
                    print::info "Found existing pyenv for user: $ACTUAL_USER (home: $ACTUAL_HOME)"
                    break
                fi
            done
            if [ -z "$ACTUAL_USER" ]; then
                error::exit "Cannot determine user for pyenv operations. Please run with sudo from a regular user account."
            fi
        fi
    fi
else
    # Running as regular user
    ACTUAL_USER="$USER"
    ACTUAL_HOME="$HOME"
    print::info "Running as regular user: $ACTUAL_USER (home: $ACTUAL_HOME)"
fi

# Debug: Show detected user info
print::info "Running as: USER=$USER, SUDO_USER=$SUDO_USER, ACTUAL_USER=$ACTUAL_USER, ACTUAL_HOME=$ACTUAL_HOME"

# PROGRESS BAR
REMAIN=" "
StepsDone=0
TotalSteps=$((${#tools[@]}+9))
####################################################################
# PROCESS
####################################################################
if ! sudo -v; then
	echo -e "${RED}This script requires sudo privileges${NC}"
	exit 1
fi

if ! grep -q "Ubuntu 24" /etc/os-release 2> /dev/null; then
	echo -e "${RED}This script requires Ubuntu 24.04 LTS${NC}"
	exit 1
fi

clear

bar::start

bar::status_changed $((StepsDone)) $TotalSteps

print::head "Updating System ..."
apt update -qq
bar::status_changed $((StepsDone++)) $TotalSteps

print::head "Upgrading System ..."
apt full-upgrade -y -qq
bar::status_changed $((StepsDone++)) $TotalSteps

print::head "Installing Build Tools ...."
for tool in "${tools[@]}"; do
	if ! apt install -y "$tool" &> /dev/null; then
		print::warn "Failed to install '$tool'"
	else
		print::success "Successfully installed '$tool'"
	fi
	bar::status_changed $((StepsDone++)) $TotalSteps
done

print::head "Cleaning Up ..."
apt autoremove -y -qq && apt clean -qq
bar::status_changed $((StepsDone++)) $TotalSteps

print::head "Creating Installation Directories ..."
for dir in "${dirs[@]}"; do
	mkdir -p "$HOME/$dir"
done
print::success "DONE!"
bar::status_changed $((StepsDone++)) $TotalSteps

print::head "Installing Alias Files ..."
install::files "$SCRIPT_DIR"/sys/lib/aliases "$HOME"/.labware/lib/aliases
print::success "DONE!"
bar::status_changed $((StepsDone++)) $TotalSteps

print::head "Installing Completion Files ..."
install::files "$SCRIPT_DIR"/sys/lib/completions "$HOME"/.labware/lib/completions
print::success "DONE!"
bar::status_changed $((StepsDone++)) $TotalSteps

print::head "Installing Function Files ..."
install::files "$SCRIPT_DIR"/sys/lib/functions "$HOME"/.labware/lib/functions
print::success "DONE!"
bar::status_changed $((StepsDone++)) $TotalSteps

print::head "Installing DOT Files ..."
mkdir -p "$HOME"/.bashrc.d/prompts
install::files "$SCRIPT_DIR"/sys/dots/.bashrc.d "$HOME"/.bashrc.d
if ! install -m 644 "$HOME"/.bashrc "$HOME"/.backup/.bashrc.OLD; then
	print::warn "Failed to backup '.bashrc'"
fi
if ! install -m 644 "$HOME"/.profile "$HOME"/.backup/.profile.OLD ; then
	print::warn "Failed to backup '.profile'"
fi
if ! install -m 644 "$SCRIPT_DIR"/sys/dots/.bashrc "$HOME"/.bashrc; then
	error::exit "Failed to install '.bashrc'"
fi
if ! install -m 644 "$SCRIPT_DIR"/sys/dots/.profile "$HOME"/.profile; then
	error::exit "Failed to install '.profile'"
else
	print::success "Done!"
fi
bar::status_changed $((StepsDone++)) $TotalSteps

print::head "Installing Hardening Config Files"
install::files "$SCRIPT_DIR"/sys/etc "$HOME"/.labware/etc
print::success "DONE!"
bar::status_changed $((StepsDone++)) $TotalSteps

bar::stop

PYENV_CMD="$ACTUAL_HOME/.pyenv/bin/pyenv"

if [ ! -d "$ACTUAL_HOME/.pyenv" ]; then
	print::head "Installing PYENV ..."
	if sudo -u "$ACTUAL_USER" bash -c 'curl -fsSL https://pyenv.run | bash'; then
		{
			echo
			echo '# Pyenv Configuration';
			echo 'export PYENV_ROOT="$HOME/.pyenv"';
			echo '[[ -d $PYENV_ROOT/bin ]] && export PATH=$PYENV_ROOT/bin:$PATH';
			echo 'eval "$(pyenv init - bash)"';
			echo '# eval "$(pyenv virtualenv-init -)"';
		} >> "$ACTUAL_HOME/.bashrc"
		{
			echo
			echo '# Pyenv Configuration';
			echo 'export PYENV_ROOT="$HOME/.pyenv"';
			echo '[[ -d $PYENV_ROOT/bin ]] && export PATH=$PYENV_ROOT/bin:$PATH';
			echo 'eval "$(pyenv init - bash)"';
			echo '# eval "$(pyenv virtualenv-init -)"';
		} >> "$ACTUAL_HOME/.profile"
	else
		error::exit "Failed to install PYENV"
	fi
	print::success "DONE!"

	print::head "Reloading Shell ..."
	# Source pyenv configuration directly instead of relying on bashrc
	export PYENV_ROOT="$ACTUAL_HOME/.pyenv"
	export PATH="$PYENV_ROOT/bin:$PATH"
	eval "$(pyenv init - bash)"
	print::success "Pyenv environment loaded!"

	# Verify pyenv is available
	if ! command -v pyenv &> /dev/null; then
		error::exit "Pyenv command not found after reload"
	fi

	print::head "Installing Python ..."
	# Use full path to pyenv to avoid PATH issues
	if ! sudo -u "$ACTUAL_USER" "$PYENV_CMD" install 3.14:latest; then
		error::exit "Failed to install Python"
	fi
	print::success "DONE!"

	print::head "Set global flags ..."
	if ! sudo -u "$ACTUAL_USER" "$PYENV_CMD" global 3.14; then
		error::exit "Failed to set global flag"
	fi

	print::head "Setting Up Virtual Environment ..."
	if [ ! -d "$ACTUAL_HOME/.pyenv/versions/labenv" ]; then
		if ! sudo -u "$ACTUAL_USER" "$PYENV_CMD" virtualenv labenv; then
			error::exit "Failed to setup virtual environment"
		fi
	fi
fi

# Activate pyenv virtual environment for script execution
print::head "Activating Virtual Environment ..."
# Debug: Show what we're trying to source
print::info "Attempting to source: $ACTUAL_HOME/.pyenv/versions/labenv/bin/activate"
# Check if the activation script exists
if [ ! -f "$ACTUAL_HOME/.pyenv/versions/labenv/bin/activate" ]; then
    print::error "Virtual environment activation script not found at: $ACTUAL_HOME/.pyenv/versions/labenv/bin/activate"
    print::info "Checking known locations..."
    # Fallback: try known locations
    if [ -f "/home/ragdata/.pyenv/versions/labenv/bin/activate" ]; then
        print::info "Found at /home/ragdata/.pyenv/versions/labenv/bin/activate - using fallback"
        source "/home/ragdata/.pyenv/versions/labenv/bin/activate"
    else
        error::exit "Cannot find virtual environment activation script"
    fi
else
    # Source the virtual environment activation script directly
    source "$ACTUAL_HOME/.pyenv/versions/labenv/bin/activate"
fi
print::success "Virtual environment activated!"

# Verify pip and python are available
if ! command -v pip &> /dev/null; then
    error::exit "pip command not found in virtual environment"
fi
if ! command -v python &> /dev/null; then
    error::exit "python command not found in virtual environment"
fi

# Check if DEV environment variable is set (default to false if not set)
DEV=${DEV:-false}

if [ "$DEV" = "true" ]; then
	pip install -e . -q
	lab install --debug
else
	pip install . -q
	lab install
fi
