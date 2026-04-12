# shellcheck shell=bash
####################################################################
# ENVIRONMENT VARIABLES
####################################################################
# License:      MIT License
# Repository:	https://github.com/Ragdata/.dotfiles
# Copyright:    Copyright © 2025 Redeyed Technologies
####################################################################
# PROMPT
export DOTFILES_PROMPT="kali"
#
# PATHS
#
export BACKUP="${HOME}/.backup"
export BASHRCD="${HOME}/.bashrc.d"
export BASEDIR="${HOME}/.labware"

export CUSTOM="${BASEDIR}/custom"
export SYSDIR="${BASEDIR}/sys"

export CFGDIR="${SYSDIR}/cfg"
export DOTSDIR="${SYSDIR}/dots"
export ETCDIR="${SYSDIR}/etc"
export LIBDIR="${SYSDIR}/lib"
export LOGDIR="${SYSDIR}/log"

export REGISTRY="${SYSDIR}/reg"

export ALIASES="${LIBDIR}/aliases"
export ASSETS="${LIBDIR}/assets"
export COMPLETIONS="${LIBDIR}/completions"
export FUNCTIONS="${LIBDIR}/functions"
export HELPDIR="${LIBDIR}/help"
export PACKAGES="${LIBDIR}/pkgs"
export PLUGINS="${LIBDIR}/plugins"
export SCRIPTS="${LIBDIR}/scripts"
export STACKS="${LIBDIR}/stacks"
export TEMPLATES="${LIBDIR}/templates"
#
# ESCAPE CHARACTERS
#
export TERM_ESC=$'\033'
export TERM_CSI="${TERM_ESC}["
export TERM_OSC="${TERM_ESC}]"
export TERM_ST="${TERM_ESC}\\"
#
# MESSAGE SYMBOLS
#
export SYMBOL_ERROR="✘"
export SYMBOL_WARNING="🛆"
export SYMBOL_INFO="✚"
export SYMBOL_SUCCESS="🗸"
export SYMBOL_TIP="★"
export SYMBOL_IMPORTANT="⚑"
export SYMBOL_HEAD="➤ "
export SYMBOL_DOT="⦁"
