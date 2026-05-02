#!/usr/bin/env bash
####################################################################
# Author:       Ragdata
# Date:         20/09/2025
# License:      MIT License
# Copyright:    Copyright © 2025 Redeyed Technologies
####################################################################
# INSTALL VIRTUALMIN
####################################################################

# Check if the script is run as root
if [ "$(id -u)" -ne 0 ]; then
	echo "This script must be run as root. Use 'sudo' to run it."
	exit 1
fi

# apt update && apt full-upgrade -y

sh -c "$(curl -fsSL https://software.virtualmin.com/gpl/scripts/virtualmin-install.sh)" -- --bundle LEMP

echo "Virtualmin has been installed successfully."
