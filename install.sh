#!/usr/bin/env bash
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
set -e

# LOCAL VARIABLES
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

. vendor/progressbar
####################################################################
# VARIABLES
####################################################################
# Color codes for output
export RED='\033[0;31m'
export GREEN='\033[0;32m'
export YELLOW='\033[0;33m'
export BLUE='\033[0;34m'
export NC='\033[0m' # No Color

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

# PROGRESSBAR
export REMAIN=" "
export StepsDone=0
export TotalSteps=$((${#tools[@]}+3))

# OPERATING VARIABLES
export DEBIAN_FRONTEND=noninteractive
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

update_server() {
	TotalSteps=$1
	StepsDone=${2:-0}

	bar::start

	bar::status_changed $((${StepsDone})) "$TotalSteps"

	print::head "Updating System ..."
	apt update -qq
	bar::status_changed $((${StepsDone}+1)) "$TotalSteps"

	print::head "Upgrading System ..."
	apt full-upgrade -y -qq
	bar::status_changed $((${StepsDone}+1)) "$TotalSteps"

	print::head "Installing Build Tools ..."
	for tool in "${tools[@]}"; do
		if ! apt install -y "$tool" &> /dev/null; then
			print::warn "Failed to install '$tool'"
		else
			print::success "Successfully installed '$tool'"
		fi
		StepsDone=$((${StepsDone:-2}+1))
		bar::status_changed "${StepsDone}" "$TotalSteps"
	done

	print::head "Cleaning up ..."
	apt autoremove -y -qq && apt clean -qq
	bar::status_changed $((${StepsDone}+1)) "$TotalSteps"

	bar::stop
}

install_files() {
	print::head "Creating Installation Directories ..."
	mkdir -p "$HOME"/.backup "$HOME"/.labware
	cd "$HOME"/.labware
	mkdir -p lib/alliases lib/completions lib/functions log reg
	cd --

	print::head "Installing Alias Files ..."
	for file in "$SCRIPT_DIR"/sys/lib/aliases/*; do
		if install -m 644 "$SCRIPT_DIR"/sys/lib/aliases/"$file" "$HOME"/.labware/lib/aliases/"$file"; then
			print::default "  - $file"
		else
			print::warn "Failed to install '$file'"
		fi
	done

	print::head "Installing Completion Files ..."
	for file in "$SCRIPT_DIR"/sys/lib/completions/*; do
		if install -m 644 "$SCRIPT_DIR"/sys/lib/completions/"$file" "$HOME"/.labware/lib/completions/"$file"; then
			print::default "  - $file"
		else
			print::warn "Failed to install '$file'"
		fi
	done

	print::head "Installing Function Files ..."
	for file in "$SCRIPT_DIR"/sys/lib/functions/*; do
		if install -m 644 "$SCRIPT_DIR"/sys/lib/functions/"$file" "$HOME"/.labware/lib/functions/"$file"; then
			print::default "  - $file"
		else
			print::warn "Failed to install '$file'"
		fi
	done

	print::head "Installing DOT Files ..."
	mkdir -p "$HOME"/.bashrc.d/prompts
	print::default "  - .bashrc.d"
	for file in "$SCRIPT_DIR"/sys/dots/.bashrc.d/*; do
		if [ ! -d "$file" ]; then
			if install -m 644 "$SCRIPT_DIR"/sys/dots/.bashrc.d/"$file"; then
				print::default "    - $file"
			else
				print::warn "Failed to install '$file'"
			fi
		fi
	done
	print::default "    - prompts"
	for file in "$SCRIPT_DIR"/sys/dots/.bashrc.d/prompts/*; do
		if install -m 644 "$SCRIPT_DIR"/sys/dots/.bashrc.d/prompts/"$file" "$HOME"/.labware/.bashrc.d/prompts/"$file"; then
			print::default "      - $file"
		else
			print::warn "Failed to install '$file'"
		fi
	done
	if ! install -m 644 "$HOME"/.bashrc "$HOME"/.backup/.bashrc.OLD; then
		print::warn "Failed to backup '$file'"
	fi
	if ! install -m 644 "$HOME"/.profile "$HOME"/.backup/.profile; then
		print::warn "Failed to backup '$file'"
	fi
	if install -m 644 "$SCRIPT_DIR"/sys/dots/.bashrc "$HOME"/.bashrc; then
		print::default "  - .bashrc"
	else
		error::exit "Failed to install '.bashrc'"
	fi
	if install -m 644 "$SCRIPT_DIR"/sys/dots/.profile "$HOME"/.profile; then
		print::default "  - .profile"
	else
		error::exit "Failed to install '.profile'"
	fi
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

update_server $TotalSteps
install_files

