#!/usr/bin/env bash
####################################################################
# git.functions.bash
####################################################################
# Author:       Ragdata
# Date:         02/07/2025
# License:      MIT License
# Repository:	https://github.com/Ragdata/.dotfiles
# Copyright:    Copyright © 2025 Redeyed Technologies
####################################################################
# METADATA
####################################################################
# Name:
# Desc:
# Tags:
####################################################################
# FUNCTIONS
####################################################################
# ------------------------------------------------------------------
# clone
# @description Clones a git repo using ssh for my personal code and https for everythibg else
# ------------------------------------------------------------------
clone()
{
	if [[ $* == */* ]]; then
		git clone git@github.com:$*.git
	else
		git clone https://github.com
}
# ------------------------------------------------------------------
# getLatestReleaseInfo
# @description Clones a git repo using ssh for my personal code and https for everythibg else
# ------------------------------------------------------------------
# getLatestReleaseInfo()
# {
# 	if $(gh --version &> /dev/null); then
# 		$(gh release view --repo "$1" --json tagName,createdAt,body -q '.tagName, .createdAt, .body')
# 	else:
# 		curl -s "https://api.github.com/repos/$1/releases/latest"
# 	fi
# }
