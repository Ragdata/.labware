# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

# If set, the pattern "**" used in a pathname expansion context will
# match all files and zero or more directories and subdirectories.
#shopt -s globstar

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# PATHS
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/"$USER"/.local/bin
export CDPATH=.:~

# set PATH so it includes user's private bin if it exists
[ -d "$HOME/bin" ] && export PATH="$HOME/bin:$PATH"

# set PATH so it includes user's private bin if it exists
[ -d "$HOME/.local/bin" ] && export PATH="$HOME/.local/bin:$PATH"

# set PATH so it includes virtual env directory if it exists
[ -d "$HOME/.venv/dotenv/bin" ] && export PATH="$HOME/.venv/dotenv/bin:$PATH"
#-------------------------------------------------------------------
# CRITICAL FUNCTIONS
#-------------------------------------------------------------------
checkOverride()
{
	srcfile="$1"

	bashindex=$(echo "$srcfile" | awk '{print index($0, "'"/.bashrc.d"'")}')
	sysindex=$(echo "$srcfile" | awk '{print index($0, "'"/sys"'")}')

	if (( $bashindex != 0 )); then
		# Source file is in .bashrc.d directory
		destfile="$CUSTOM/dots/.bashrc.d/$(basename "$srcfile")"
	elif (( $sysindex != 0 )); then
		# Source file is in .dotfiles/sys directory
		destfile="$CUSTOM/${srcfile#$SYSDIR/}"
	else
		echo "$srcfile"
	fi
	# Determine if override file exists
	if [[ -f "$destfile" ]]; then
		echo "$destfile"
	else
		echo "$srcfile"
	fi
}
#-------------------------------------------------------------------
# SETUP SHELL
#-------------------------------------------------------------------
# First make sure ~/.bash_history has not been truncated
if [[ $(wc -l ~/.bash_history | awk '{print $1}') -lt 500 ]]; then
	echo "NOTE: ~/.bash_history appears to have been truncated. Please check your shell configuration."
fi

# History Settings
HISTCONTROL=ignoreboth:erasedups
HISTFILE=$HOME/.bash_history
HISTFILESIZE=99999
HISTIGNORE=?:??
HISTSIZE=99999

# Enable useful shell options:
#  - autocd - change directory without no need to type 'cd' when changing directory
#  - cdspell - automatically fix directory typos when changing directory
#  - direxpand - automatically expand directory globs when completing
#  - dirspell - automatically fix directory typos when completing
#  - globstar - ** recursive glob
#  - histappend - append to history, don't overwrite
#  - histverify - expand, but don't automatically execute, history expansions
#  - nocaseglob - case-insensitive globbing
#  - no_empty_cmd_completion - do not TAB expand empty lines
shopt -s autocd cdspell direxpand dirspell globstar histappend histverify nocaseglob no_empty_cmd_completion

# Prevent file overwrite on stdout redirection.
# Use `>|` to force redirection to an existing file.
set -o noclobber

# Only logout if 'Control-d' is executed two consecutive times.
export IGNOREEOF=1

# Set preferred umask.
umask 022

# Disable Alacritty icon bouncing for interactive shells.
# Refer to: https://is.gd/8MPdGh
if [[ $- =~ i ]]; then
	printf "\e[?1042l"
fi
# PROMPT_COMMAND='history -a'

# iterate through the folders in the .bashrc.d directory
# and make sure that everything gets to where it ought to be.
include()
{
	for script in "$1"/*
	do
		[[ ! -f "$script" && ! -L "$script" ]] && continue
		# Check for an override file
		script=$(checkOverride "$script")
		# Check if the file is a symlink
		[[ -L "$script" ]] && script=$(readlink -f "$script")
		# Source the script
		source "$script" || { echo "Error sourcing script: $script"; continue; }
	done
}

[ -d "$HOME/.bashrc.d" ] && include "$HOME/.bashrc.d"
# EOF ##############################################################
