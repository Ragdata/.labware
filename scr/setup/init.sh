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

echo -e "${YELLOW}Updating System ...${NC}"
apt update

echo -e "${YELLOW}Upgrading System ...${NC}"
apt full-upgrade -y

echo -e "${YELLOW}Install Essential Tools ...${NC}"
apt install -y curl wget git gnupg2 net-tools dnsutils iputils-ping procps python3-full python3-pip

echo -e "${YELLOW}Installing UV ...${NC}"
curl -LsSf https://astral.sh/uv/install.sh | sh

echo -e "${YELLOW}Installing Python Libraries ...${NC}"
pip install -r requirements.txt --user --break-system-packages
