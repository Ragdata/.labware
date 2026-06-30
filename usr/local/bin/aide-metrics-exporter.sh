#!/bin/bash
# Copyright (c) 2025-2026 Marc Allgeier (fidpa)
# SPDX-License-Identifier: MIT
# https://github.com/fidpa/ubuntu-server-security
#
# AIDE Metrics Exporter for Prometheus
#
# Exports AIDE database metrics in Prometheus textfile collector format.
# Enables monitoring of AIDE database age, size, and check status via Grafana.
#
# Features:
# - Prometheus textfile collector format
# - Atomic writes (temp file + rename)
# - Graceful degradation when database is missing
# - No external dependencies
#
# Metrics:
#   aide_db_size_bytes - Database size in bytes
#   aide_db_age_seconds - Age of database since last update
#   aide_last_update_timestamp - UNIX timestamp of last update
#   aide_last_check_status - Last check status (0=OK, 1=WARNING, 2=CRITICAL)
#
# Usage:
#   ./aide-metrics-exporter.sh
#
# Prometheus node_exporter setup:
#   1. Install node_exporter with --collector.textfile.directory=/var/lib/node_exporter/textfile_collector
#   2. Run this script after AIDE updates (via ExecStartPost in systemd service)
#   3. Query metrics: aide_db_age_seconds > 90000 (alert if DB > 25 hours old)
#
# Exit Codes:
#   0 - Success
#   1 - Warning (database not found, metrics set to -1)
#
# Documentation: https://github.com/fidpa/ubuntu-server-security/docs/PROMETHEUS_INTEGRATION.md
# Version: 1.0.0
# Created: 2026-01-04

set -uo pipefail

# ============================================
# Configuration
# ============================================

AIDE_DB="${AIDE_DB:-/var/lib/aide/aide.db}"
METRICS_FILE="${METRICS_FILE:-/var/lib/node_exporter/textfile_collector/aide.prom}"
LOG_FILE="${LOG_FILE:-/var/log/aide/metrics.log}"

# Status codes
STATUS_OK=0
STATUS_WARNING=1
STATUS_CRITICAL=2

# ============================================
# Functions
# ============================================

log() {
    local level="$1"
    shift
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] [$level] $*" | tee -a "$LOG_FILE" 2>/dev/null || true
}

error() {
    log "ERROR" "$@" >&2
}

get_db_size() {
    if [[ -f "$AIDE_DB" ]]; then
        stat -c%s "$AIDE_DB" 2>/dev/null || echo "-1"
    else
        echo "-1"
    fi
}

get_db_age() {
    if [[ -f "$AIDE_DB" ]]; then
        local mtime now age
        mtime=$(stat -c%Y "$AIDE_DB" 2>/dev/null) || { echo "-1"; return 1; }
        now=$(date +%s)
        age=$((now - mtime))
        echo "$age"
    else
        echo "-1"
    fi
}

get_db_timestamp() {
    if [[ -f "$AIDE_DB" ]]; then
        stat -c%Y "$AIDE_DB" 2>/dev/null || echo "0"
    else
        echo "0"
    fi
}

determine_status() {
    local age="$1"

    # Database missing
    if [[ $age -eq -1 ]]; then
        echo "$STATUS_CRITICAL"
        return
    fi

    # Database older than 25 hours (90000 seconds)
    if [[ $age -gt 90000 ]]; then
        echo "$STATUS_WARNING"
        return
    fi

    # All good
    echo "$STATUS_OK"
}

write_metrics() {
    local db_size db_age db_timestamp status

    db_size=$(get_db_size)
    db_age=$(get_db_age)
    db_timestamp=$(get_db_timestamp)
    status=$(determine_status "$db_age")

    # Create metrics directory
    local metrics_dir
    metrics_dir="$(dirname "$METRICS_FILE")"
    if [[ ! -d "$metrics_dir" ]]; then
        log "INFO" "Creating metrics directory: $metrics_dir"
        mkdir -p "$metrics_dir" || { error "Failed to create metrics directory"; return 1; }
    fi

    # Atomic write (temp file + rename)
    local temp_file="${METRICS_FILE}.$$"

    cat > "$temp_file" <<EOF
# HELP aide_db_size_bytes AIDE database size in bytes
# TYPE aide_db_size_bytes gauge
aide_db_size_bytes $db_size

# HELP aide_db_age_seconds Age of AIDE database in seconds
# TYPE aide_db_age_seconds gauge
aide_db_age_seconds $db_age

# HELP aide_last_update_timestamp UNIX timestamp of last AIDE database update
# TYPE aide_last_update_timestamp gauge
aide_last_update_timestamp $db_timestamp

# HELP aide_last_check_status Last AIDE check status (0=OK, 1=WARNING, 2=CRITICAL)
# TYPE aide_last_check_status gauge
aide_last_check_status $status
EOF

    # Atomic move
    mv "$temp_file" "$METRICS_FILE" || { error "Failed to write metrics file"; rm -f "$temp_file"; return 1; }

    # Fix permissions (readable by node_exporter)
    chmod 644 "$METRICS_FILE"

    log "INFO" "Metrics exported: size=${db_size}B, age=${db_age}s, status=${status}"
}

# ============================================
# Main
# ============================================

main() {
    log "INFO" "Exporting AIDE metrics to $METRICS_FILE"

    if ! write_metrics; then
        error "Failed to export metrics"
        exit 1
    fi

    log "INFO" "Metrics export completed successfully"
}

main "$@"
