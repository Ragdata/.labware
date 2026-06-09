#!/usr/bin/env bash
# shellcheck disable=SC2034
####################################################################
# 0.init.sh
####################################################################
# Author:       Ragdata
# Date:         06/05/2026
# License:      MIT License
# Repository:	https://github.com/Ragdata/.dotfiles
# Copyright:    Copyright © 2026 Redeyed Technologies
####################################################################
# PRE-FLIGHT
####################################################################
# set -x
# BASEDIR="$(cd -P "$(dirname "$(dirname "$(dirname "$(realpath "${BASH_SOURCE[0]}")")")")" >/dev/null 2>&1 && pwd)"

####################################################################
# VARIABLES
####################################################################
# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

####################################################################
# FUNCTIONS
####################################################################
lw::copyTree()
{
    local src=$1
    local dst=$2

    if [ -f "$src" ]; then
        echo -e "${RED}Source $src is a file, not a directory.${NC}"
        exit 1
    elif [ ! -d "$src" ]; then
        echo -e "${RED}Directory $src does not exist.${NC}"
        exit 1
    fi
    if [ -f "$dst" ]; then
        echo -e "${RED}Destination $dst is a file, not a directory.${NC}"
        exit 1
    elif [ ! -d "$dst" ]; then
        echo -e "${YELLOW}Destination $dst does not exist. Creating...${NC}"
        mkdir -p "$dst"
    fi
    if rsync -av --exclude='.git' --exclude='*.log' "$src/" "$dst/"; then
        echo -e "${GREEN}Successfully copied $src to $dst.${NC}"
    else
        echo -e "${RED}Failed to copy $src to $dst.${NC}"
        exit 1
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

echo -e "${YELLOW}Adding Repositories${NC}"
add-apt-repository -y ppa:deadsnakes/ppa
add-apt-repository -y ppa:git-core/ppa

echo
echo -e "${YELLOW}Updating System ...${NC}"
apt update

echo
echo -e "${YELLOW}Upgrading System ...${NC}"
apt full-upgrade -y

echo
echo -e "${YELLOW}Install Essential Tools ...${NC}"
apt install -y curl wget git gnupg2 net-tools dnsutils iputils-ping procps python3.14-full python3.14-venv

# echo -e "${YELLOW}Installing UV ...${NC}"
# curl -LsSf https://astral.sh/uv/install.sh | sh

if ! which python3.14 > /dev/null 2>&1; then
    apt install -y python3.14-full python3.14-venv
fi

echo
echo -e "${YELLOW}Installing Python Package and Dependencies in dev mode ...${NC}"
python3.14 -m pip install -e . --break-system-packages
python3.14 -m pip install ".[dev]" --break-system-packages
python3.14 -m pip install ".[docs]" --break-system-packages

echo
echo -e "${YELLOW}Installing Labware Scripts ...${NC}"
lw::copyTree "scr" "/opt/labware"
lw::copyTree "svc" "/opt/labware/svc"
lw::copyTree "sys" "/opt/labware/sys"
lw::copyTree "usr/local/bin" "/usr/local/bin"

echo
echo -e "${YELLOW}Installing Bash Production Toolkit ...${NC}"
git clone https://github.com/fidpa/bash-production-toolkit.git /tmp/bash-production-toolkit
bash /tmp/bash-production-toolkit/install.sh --prefix /usr/local/lib/bash-production-toolkit
rm -rf /tmp/bash-production-toolkit
