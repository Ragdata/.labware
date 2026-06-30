#!/bin/bash
# Copyright (c) 2025-2026 Marc Allgeier (fidpa)
# SPDX-License-Identifier: MIT
# https://github.com/fidpa/ubuntu-server-security
#
# AIDE Database Backup Script
#
# Creates offsite backups of AIDE database with 30-day retention.
# This is critical for intrusion detection: a compromised system can disable
# local AIDE, so offsite backups allow post-incident forensics.
#
# Features:
# - Atomic operations (temp file + rename)
# - 30-day retention policy
# - Privilege separation (runs as user, uses sudo internally)
# - Validation before backup
#
# Usage:
#   ./backup-aide-db.sh
#
# Exit Codes:
#   0 - Success
#   1 - Warning (database not found)
#   2 - Error
#
# Documentation: https://github.com/fidpa/ubuntu-server-security/docs/BEST_PRACTICES.md
# Version: 1.0.0
# Created: 2026-01-04

set -uo pipefail

# ============================================
# Configuration
# ============================================

AIDE_DB="${AIDE_DB:-/var/lib/aide/aide.db}"
BACKUP_DIR="${BACKUP_DIR:-/var/backups/aide-offsite}"
RETENTION_DAYS="${RETENTION_DAYS:-30}"

LOG_FILE="${LOG_FILE:-/var/log/aide/backup.log}"

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
    # Check if AIDE database exists
    if [[ ! -f "$AIDE_DB" ]]; then
        die 1 "AIDE database not found: $AIDE_DB"
    fi

    # Create backup directory
    mkdir -p "$BACKUP_DIR" || die 2 "Failed to create backup directory: $BACKUP_DIR"
    chmod 750 "$BACKUP_DIR"

    # Create log directory
    local log_dir
    log_dir="$(dirname "$LOG_FILE")"
    mkdir -p "$log_dir" || die 2 "Failed to create log directory: $log_dir"
}

create_backup() {
    local timestamp
    timestamp="$(date +'%Y%m%d_%H%M%S')"
    local backup_file="${BACKUP_DIR}/aide.db.${timestamp}"
    local temp_file="${BACKUP_DIR}/.aide.db.${timestamp}.tmp"

    log "INFO" "Creating backup: $backup_file"

    # Check if we need sudo to read the database
    if [[ ! -r "$AIDE_DB" ]]; then
        # Use sudo to copy
        if ! sudo cp -a "$AIDE_DB" "$temp_file" 2>>"$LOG_FILE"; then
            die 2 "Failed to backup database (permission denied)"
        fi

        # Change ownership to current user for further processing
        sudo chown "$(id -u):$(id -g)" "$temp_file"
    else
        # Direct copy (no sudo needed)
        if ! cp -a "$AIDE_DB" "$temp_file" 2>>"$LOG_FILE"; then
            die 2 "Failed to backup database"
        fi
    fi

    # Atomic move
    mv "$temp_file" "$backup_file" || die 2 "Failed to finalize backup"

    # Verify backup
    if [[ ! -f "$backup_file" ]]; then
        die 2 "Backup verification failed: $backup_file not found"
    fi

    local backup_size
    backup_size=$(stat -c%s "$backup_file")
    log "INFO" "Backup created successfully (${backup_size} bytes)"
}

cleanup_old_backups() {
    log "INFO" "Cleaning up backups older than ${RETENTION_DAYS} days"

    local deleted_count=0
    while IFS= read -r -d '' file; do
        log "INFO" "Deleting old backup: $file"
        rm "$file"
        ((deleted_count++))
    done < <(find "$BACKUP_DIR" -name 'aide.db.*' -type f -mtime +"$RETENTION_DAYS" -print0)

    if [[ $deleted_count -gt 0 ]]; then
        log "INFO" "Deleted $deleted_count old backup(s)"
    else
        log "INFO" "No old backups to delete"
    fi
}

# ============================================
# Main
# ============================================

main() {
    log "INFO" "Starting AIDE database backup"

    # Preflight checks
    check_requirements

    # Create backup
    create_backup

    # Cleanup old backups
    cleanup_old_backups

    log "INFO" "AIDE database backup completed successfully"
}

main "$@"
