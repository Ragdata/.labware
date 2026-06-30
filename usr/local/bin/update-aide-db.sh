#!/bin/bash
# Copyright (c) 2025-2026 Marc Allgeier (fidpa)
# SPDX-License-Identifier: MIT
# https://github.com/fidpa/ubuntu-server-security
#
# AIDE Database Update Script
#
# Updates the AIDE database after system changes, with validation and backup.
# Based on production servers with 100% CIS Benchmark compliance.
#
# Features:
# - Permission management (root:_aide 640/750 for non-root monitoring)
# - Immutable binary protection (chattr +i handling)
# - Disk space validation
# - Backup before update
# - Timeout protection
# - Semantic exit codes
# - Vaultwarden integration (optional, with .env fallback)
#
# Usage:
#   sudo ./update-aide-db.sh              # Interactive mode
#   sudo ./update-aide-db.sh --check      # Check only (no update)
#   sudo ./update-aide-db.sh --post-upgrade  # Silent mode (for APT hooks)
#
# Exit Codes:
#   0 - Success (database updated)
#   1 - Warnings (changes detected, review before updating)
#   2 - Critical error
#   3 - Permission error
#   4 - Insufficient disk space
#
# Documentation: https://github.com/fidpa/ubuntu-server-security/docs/SETUP.md
# Version: 2.0.0
# Created: 2026-01-04

set -uo pipefail

# ============================================
# Configuration
# ============================================

AIDE_BINARY="${AIDE_BINARY:-/usr/bin/aide}"
AIDE_CONFIG="${AIDE_CONFIG:-/etc/aide/aide.conf}"
AIDE_DB="${AIDE_DB:-/var/lib/aide/aide.db}"
AIDE_DB_NEW="${AIDE_DB_NEW:-/var/lib/aide/aide.db.new}"
AIDE_DB_DIR="$(dirname "$AIDE_DB")"
AIDE_GROUP="${AIDE_GROUP:-_aide}"

# Logging
LOG_DIR="${LOG_DIR:-/var/log/aide}"
LOG_FILE="${LOG_DIR}/update.log"

# Backup
BACKUP_DIR="${BACKUP_DIR:-/var/backups/aide}"
BACKUP_RETENTION="${BACKUP_RETENTION:-10}"

# Timeouts
AIDE_TIMEOUT="${AIDE_TIMEOUT:-2700}"  # 45 minutes

# Disk space (in MB)
MIN_DISK_SPACE="${MIN_DISK_SPACE:-100}"

# Mode flags
MODE="interactive"
CHECK_ONLY=false

# ============================================
# Vaultwarden Integration (Optional)
# ============================================
# Source Vaultwarden credentials library if available
# This provides get_credential() and related functions
SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
VAULTWARDEN_LIB="${SCRIPT_DIR}/../../vaultwarden/vaultwarden-credentials.sh"

if [[ -f "$VAULTWARDEN_LIB" ]]; then
    # shellcheck source=../../vaultwarden/vaultwarden-credentials.sh
    source "$VAULTWARDEN_LIB"
fi

# ============================================
# Functions
# ============================================

log() {
    local level="$1"
    shift
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] [$level] $*" | tee -a "$LOG_FILE"
}

error() {
    log "ERROR" "$@" >&2
}

die() {
    local exit_code=$1
    shift
    error "$@"
    exit "$exit_code"
}

check_requirements() {
    # Check if running as root
    if [[ $EUID -ne 0 ]]; then
        die 3 "This script must be run as root"
    fi

    # Check AIDE binary exists
    if [[ ! -x "$AIDE_BINARY" ]]; then
        die 2 "AIDE binary not found or not executable: $AIDE_BINARY"
    fi

    # Check AIDE config exists
    if [[ ! -f "$AIDE_CONFIG" ]]; then
        die 2 "AIDE configuration not found: $AIDE_CONFIG"
    fi

    # Create log directory
    mkdir -p "$LOG_DIR"
    chmod 750 "$LOG_DIR"

    # Create backup directory
    mkdir -p "$BACKUP_DIR"
    chmod 750 "$BACKUP_DIR"
}

check_disk_space() {
    local available_mb
    available_mb=$(df -BM "$AIDE_DB_DIR" | awk 'NR==2 {print $4}' | sed 's/M//')

    if [[ $available_mb -lt $MIN_DISK_SPACE ]]; then
        die 4 "Insufficient disk space: ${available_mb}MB available, ${MIN_DISK_SPACE}MB required"
    fi

    log "INFO" "Disk space check passed: ${available_mb}MB available"
}

remove_immutable() {
    local file="$1"

    if [[ -f "$file" ]]; then
        if lsattr "$file" 2>/dev/null | grep -q '\-i\-'; then
            log "INFO" "Removing immutable flag from $file"
            chattr -i "$file" || error "Failed to remove immutable flag from $file"
        fi
    fi
}

restore_immutable() {
    local file="$1"

    if [[ -f "$file" ]]; then
        log "INFO" "Restoring immutable flag on $file"
        chattr +i "$file" || error "Failed to restore immutable flag on $file"
    fi
}

backup_database() {
    if [[ ! -f "$AIDE_DB" ]]; then
        log "INFO" "No existing database to backup"
        return 0
    fi

    local backup_file="${BACKUP_DIR}/aide.db.$(date +'%Y%m%d_%H%M%S')"

    log "INFO" "Backing up database to $backup_file"
    cp -a "$AIDE_DB" "$backup_file" || die 2 "Failed to backup database"

    # Cleanup old backups
    log "INFO" "Cleaning up old backups (keeping last $BACKUP_RETENTION)"
    find "$BACKUP_DIR" -name 'aide.db.*' -type f | sort -r | tail -n +$((BACKUP_RETENTION + 1)) | xargs -r rm
}

run_aide_check() {
    log "INFO" "Running AIDE check (timeout: ${AIDE_TIMEOUT}s)"

    local aide_exit_code=0
    timeout "$AIDE_TIMEOUT" "$AIDE_BINARY" --check --config="$AIDE_CONFIG" 2>&1 | tee -a "$LOG_FILE" || aide_exit_code=$?

    # AIDE exit codes (from man aide):
    # 0   = no changes
    # 1-7 = changes detected (all valid scenarios)
    # 8-13 = undefined
    # 14  = write error
    # 15  = invalid argument
    # 124 = timeout

    if [[ $aide_exit_code -eq 124 ]]; then
        die 2 "AIDE check timed out after ${AIDE_TIMEOUT}s"
    elif [[ $aide_exit_code -ge 14 ]]; then
        die 2 "AIDE check failed with exit code $aide_exit_code"
    elif [[ $aide_exit_code -ge 8 ]]; then
        error "AIDE check returned undefined exit code $aide_exit_code"
        return 1
    fi

    return $aide_exit_code
}

run_aide_update() {
    log "INFO" "Running AIDE database update (timeout: ${AIDE_TIMEOUT}s)"

    local aide_exit_code=0
    timeout "$AIDE_TIMEOUT" "$AIDE_BINARY" --update --config="$AIDE_CONFIG" 2>&1 | tee -a "$LOG_FILE" || aide_exit_code=$?

    if [[ $aide_exit_code -eq 124 ]]; then
        die 2 "AIDE update timed out after ${AIDE_TIMEOUT}s"
    elif [[ $aide_exit_code -ge 14 ]]; then
        die 2 "AIDE update failed with exit code $aide_exit_code"
    fi

    if [[ ! -f "$AIDE_DB_NEW" ]]; then
        die 2 "AIDE update did not create new database: $AIDE_DB_NEW"
    fi

    return 0
}

fix_permissions() {
    # Permission pattern for non-root monitoring (Prometheus, health-checks, etc.)
    # root:_aide with 640 allows monitoring tools to read without running as root

    log "INFO" "Fixing permissions for non-root monitoring"

    # Create _aide group if it doesn't exist
    if ! getent group "$AIDE_GROUP" >/dev/null; then
        log "INFO" "Creating group $AIDE_GROUP"
        groupadd --system "$AIDE_GROUP" || error "Failed to create group $AIDE_GROUP"
    fi

    # Fix database permissions
    if [[ -f "$AIDE_DB" ]]; then
        chown root:"$AIDE_GROUP" "$AIDE_DB"
        chmod 640 "$AIDE_DB"
    fi

    # Fix database directory permissions
    chown root:"$AIDE_GROUP" "$AIDE_DB_DIR"
    chmod 750 "$AIDE_DB_DIR"

    log "INFO" "Permissions fixed: ${AIDE_DB} is now readable by group ${AIDE_GROUP}"
}

activate_database() {
    log "INFO" "Activating new database"

    # Backup old database
    backup_database

    # Atomic move
    mv "$AIDE_DB_NEW" "$AIDE_DB" || die 2 "Failed to activate new database"

    # Fix permissions
    fix_permissions

    log "INFO" "Database activated successfully"
}

# ============================================
# Main
# ============================================

main() {
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --check)
                CHECK_ONLY=true
                shift
                ;;
            --post-upgrade)
                MODE="silent"
                shift
                ;;
            --help)
                cat <<EOF
AIDE Database Update Script

Usage: $0 [OPTIONS]

Options:
  --check          Check only (no database update)
  --post-upgrade   Silent mode (for APT hooks)
  --help           Show this help

Exit Codes:
  0 - Success
  1 - Warnings (changes detected, review before updating)
  2 - Critical error
  3 - Permission error
  4 - Insufficient disk space

Documentation: https://github.com/fidpa/ubuntu-server-security/docs/SETUP.md
EOF
                exit 0
                ;;
            *)
                error "Unknown option: $1"
                exit 2
                ;;
        esac
    done

    log "INFO" "Starting AIDE database update (mode: $MODE)"

    # Preflight checks
    check_requirements
    check_disk_space

    # Setup trap for immutable protection
    # This ensures immutable flags are restored even on error
    local immutable_files=("$AIDE_BINARY" "$AIDE_CONFIG")
    trap 'for f in "${immutable_files[@]}"; do restore_immutable "$f"; done' EXIT

    # Remove immutable flags
    for file in "${immutable_files[@]}"; do
        remove_immutable "$file"
    done

    # Run AIDE check
    local check_exit_code=0
    run_aide_check || check_exit_code=$?

    if [[ $check_exit_code -eq 0 ]]; then
        log "INFO" "No changes detected"
        exit 0
    elif [[ $check_exit_code -ge 1 && $check_exit_code -le 7 ]]; then
        log "INFO" "Changes detected (AIDE exit code: $check_exit_code)"

        if [[ "$CHECK_ONLY" == "true" ]]; then
            log "INFO" "Check-only mode, exiting without update"
            exit 1
        fi

        # Update database
        run_aide_update

        if [[ "$MODE" == "interactive" ]]; then
            log "INFO" "Review changes in $LOG_FILE before activating database"
            log "INFO" "To activate: sudo mv $AIDE_DB_NEW $AIDE_DB"
            exit 1
        else
            # Silent mode (APT hook): auto-activate
            activate_database
            exit 0
        fi
    else
        # Unexpected exit code
        die 2 "AIDE check failed unexpectedly (exit code: $check_exit_code)"
    fi
}

main "$@"
