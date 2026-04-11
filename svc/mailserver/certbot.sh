#!/usr/bin/env bash
####################################################################
# Author:       Ragdata
# Date:         26/01/2026
# License:      MIT License
# Copyright:    Copyright © 2026 Redeyed Technologies
####################################################################
# INITIALISE CERTBOT
####################################################################
HOSTDIR=/opt/mailserver
HOSTNAME=mail.redeyed.au

docker run \
	--volume "${HOSTDIR}/certbot/certs/:/etc/letsencrypt/" \
	--volume "${HOSTDIR}/certbot/logs/:/var/log/letsencrypt/" \
	--volume "${HOSTDIR}/certbot/secrets/cloudflare.ini:/tmp/secrets/certbot/cloudflare.ini" \
	certbot/dns-cloudflare -v certonly --dns-cloudflare \
	--dns-cloudflare-credentials /tmp/secrets/certbot/cloudflare.ini -d ${HOSTNAME} \
	--non-interactive --agree-tos

