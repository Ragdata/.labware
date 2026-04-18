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

# PROGRESS BAR
REMAIN=" "
StepsDone=0
TotalSteps=$((${#tools[@]}+8))
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
for file in "$SCRIPT_DIR"/sys/lib/aliases/*; do
	if ! install -m 644 "$file" "$HOME"/.labware/lib/aliases/"$(basename "$file")"; then
		print::warn "Failed to install '$file'"
	fi
done
print::success "DONE!"
bar::status_changed $((StepsDone++)) $TotalSteps

print::head "Installing Completion Files ..."
for file in "$SCRIPT_DIR"/sys/lib/completions/*; do
	if ! install -m 644 "$file" "$HOME"/.labware/lib/completions/"$(basename "$file")"; then
		print::warn "Failed to install '$file'"
	fi
done
print::success "DONE!"
bar::status_changed $((StepsDone++)) $TotalSteps

print::head "Installing Function Files ..."
for file in "$SCRIPT_DIR"/sys/lib/functions/*; do
	if ! install -m 644 "$file" "$HOME"/.labware/lib/functions/"$(basename "$file")"; then
		print::warn "Failed to install '$file'"
	fi
done
print::success "DONE!"
bar::status_changed $((StepsDone++)) $TotalSteps

print::head "Installing DOT Files ..."
mkdir -p "$HOME"/.bashrc.d/prompts
for file in "$SCRIPT_DIR"/sys/dots/.bashrc.d/*; do
	if [ ! -d "$file" ]; then
		if ! install -m 644 "$file" "$HOME"/.bashrc.d/"$(basename "$file")"; then
			print::warn "Failed to install '$file'"
		fi
	fi
done
for file in "$SCRIPT_DIR"/sys/dots/.bashrc.d/prompts/*; do
	if ! install -m 644 "$file" "$HOME"/.bashrc.d/prompts/"$(basename "$file")"; then
		print::warn "Failed to install '$file'"
	fi
done
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

if [ ! -d "$HOME/.pyenv" ]; then
	print::head "Installing PYENV ..."
	if curl -fsSL https://pyenv.run | bash; then
		{
			echo
			echo '# Pyenv Configuration';
			echo 'export PYENV_ROOT="$HOME/.pyenv"';
			echo '[[ -d $PYENV_ROOT/bin ]] && export PATH=$PYENV_ROOT/bin:$PATH';
			echo 'eval "$(pyenv init - bash)"';
			echo '# eval "$(pyenv virtualenv-init -)"';
		} >> ~/.bashrc
		{
			echo
			echo '# Pyenv Configuration';
			echo 'export PYENV_ROOT="$HOME/.pyenv"';
			echo '[[ -d $PYENV_ROOT/bin ]] && export PATH=$PYENV_ROOT/bin:$PATH';
			echo 'eval "$(pyenv init - bash)"';
			echo '# eval "$(pyenv virtualenv-init -)"';
		} >> ~/.profile
	else
		error::exit "Failed to install PYENV"
	fi
	print::success "DONE!"
	bar::status_changed $((StepsDone++)) $TotalSteps

	print::head "Reloading Shell ..."
	if ! source ~/.bashrc; then
		error::exit "Failed to reload shell"
	fi
	print::success "DONE!"
	bar::status_changed $((StepsDone++)) $TotalSteps

	print::head "Installing Python ..."
	if ! pyenv 3.14:latest; then
		error::exit "Failed to install Python"
	fi
	print::success "DONE!"
	bar::status_changed $((StepsDone++)) $TotalSteps

	print::head "Set global flags ..."
	if ! pyenv global 3.14; then
		error::exit "Failed to set global flag"
	fi

	print::head "Setting Up Virtual Environment ..."
	if [ ! -d "$HOME/.pyenv/versions/labenv" ]; then
		if ! pyenv virtualenv labenv; then
			error::exit "Failed to setup virtual environment"
		fi
		bar::status_changed $((StepsDone++)) $TotalSteps
	fi
fi

pyenv activate labenv

if "$DEV"; then
	pip install -e . -q
	lab install --debug
else
	pip install . -q
	lab install
fi
bar::status_changed $((StepsDone++)) $TotalSteps

bar::stop
