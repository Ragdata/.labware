# shellcheck shell=bash
# shellcheck disable=SC2139
####################################################################
# filesys.aliases.bash
####################################################################
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
# FILESYSTEM ALIASES
####################################################################
if [ -x /usr/bin/dircolors ]; then
    if [ -r ~/.dircolors ]; then
    	eval "$(dircolors -b ~/.dircolors)"
    else
    	eval "$(dircolors -b)"
	fi
    alias ls='ls --color=auto'
fi

# movement
alias back='cd -'
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'

# guard rails
# alias rm='rm -i'
# alias mv='mv -i'
# alias cp='cp -i'
# alias ln='ln -i'
alias mkdir='mkdir -p'

# ls aliases
alias cls="clear;ll"
