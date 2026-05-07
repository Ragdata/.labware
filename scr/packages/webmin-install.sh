#!/usr/bin/env bash
####################################################################
# Author:       Ragdata
# Date:         20/09/2025
# License:      MIT License
# Copyright:    Copyright © 2025 Redeyed Technologies
####################################################################
# INSTALL WEBMIN
####################################################################

# Check if the script is run as root
if [ "$(id -u)" -ne 0 ]; then
	echo "This script must be run as root. Use 'sudo' to run it."
	exit 1
fi

apt update && apt full-upgrade -y

curl -o webmin-setup-repo.sh https://raw.githubusercontent.com/webmin/webmin/master/webmin-setup-repo.sh

sh webmin-setup-repo.sh

apt install -y webmin --install-recommends

echo "Webmin has been installed successfully."
