# shellcheck shell=bash
####################################################################
# PLUGIN LOADER
####################################################################
# License:      MIT License
# Repository:	https://github.com/Ragdata/.dotfiles
# Copyright:    Copyright © 2025 Redeyed Technologies
####################################################################

# ------------------------------------------------------------------
# loadPlugins
# ------------------------------------------------------------------
# @description Load all enabled plugin files
# ------------------------------------------------------------------
# Load all enabled plugin files
if [ -f "$REGISTRY/comp/plugins.enabled" ]; then
    while IFS= read -r line
    do
        # shellcheck disable=SC1090
        if [[ "${line:0:1}" != "#" && -n "$line" ]]; then
			script="$PLUGINS/$line/plugin.bash"
			file=$(checkOverride "$script")
            [ -f "$file" ] && source "$file"
        fi
    done < "$REGISTRY/comp/plugins.enabled"
fi
# ------------------------------------------------------------------
