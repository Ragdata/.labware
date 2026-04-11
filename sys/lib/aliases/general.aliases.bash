# shellcheck shell=bash
# shellcheck disable=SC2139
####################################################################
# general.aliases.bash
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
# GENERAL ALIASES
####################################################################
# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

# Add an "alert" alias for long running commands.  Use like so:
#   sleep 10; alert
# alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'

# maintain scrollback on clear
alias clear='clear -x'

# general utils
alias fuck=''	# As in, "FUCK, I forgot to sudo that command!"
####################################################################
# GENERAL ALIASES
####################################################################
