#!/bin/bash
#
# AIDE Failure Alert Script
# Sends Telegram alert when AIDE service fails
# Triggered via systemd OnFailure hook
#
# Version: 1.0
# Dependencies: bash-production-toolkit (alerts.sh, logging.sh)
#

set -euo pipefail

# ============================================================================
# Configuration
# ============================================================================

# Bash Production Toolkit path (override via environment variable)
BASH_TOOLKIT_PATH="${BASH_TOOLKIT_PATH:-/usr/local/lib/bash-production-toolkit}"

# Import libraries from bash-production-toolkit
# shellcheck source=/usr/local/lib/bash-production-toolkit/src/foundation/logging.sh
source "${BASH_TOOLKIT_PATH}/src/foundation/logging.sh"
# shellcheck source=/usr/local/lib/bash-production-toolkit/src/foundation/secure-file-utils.sh
source "${BASH_TOOLKIT_PATH}/src/foundation/secure-file-utils.sh"
# shellcheck source=/usr/local/lib/bash-production-toolkit/src/monitoring/alerts.sh
source "${BASH_TOOLKIT_PATH}/src/monitoring/alerts.sh"

# Environment (for alerts.sh)
# Override these via systemd service file or shell environment
export TELEGRAM_PREFIX="${TELEGRAM_PREFIX:-[🚨 AIDE]}"
export STATE_DIR="${STATE_DIR:-/var/lib/aide}"
export RATE_LIMIT_SECONDS="${RATE_LIMIT_SECONDS:-3600}"  # 1h Rate Limit (critical!)

# ============================================================================
# Main
# ============================================================================

main() {
    log_info "=========================================="
    log_info "AIDE Failure Alert"
    log_info "=========================================="

    # Get service status
    local exit_code
    exit_code=$(systemctl show aide-update.service -p ExecMainStatus --value)

    local active_state
    active_state=$(systemctl show aide-update.service -p ActiveState --value)

    local sub_state
    sub_state=$(systemctl show aide-update.service -p SubState --value)

    log_info "Service Status: ActiveState=${active_state}, SubState=${sub_state}, ExitCode=${exit_code}"

    # Get hostname for device identification
    local hostname
    hostname=$(hostname -f 2>/dev/null || hostname)

    # Construct alert message
    local alert_msg
    alert_msg="⚠️ AIDE File Integrity Check FAILED!

🖥️ Device: ${hostname}
❌ Status: ${active_state} (${sub_state})
🔢 Exit Code: ${exit_code}
⏰ Time: $(date '+%Y-%m-%d %H:%M:%S')

⚡ Critical: File Integrity Monitoring non-functional!

📋 Logs:
journalctl -u aide-update.service -n 50

🔧 Check:
systemctl status aide-update.service
ls -lh /var/lib/aide/aide.db*"

    # Load Telegram configuration
    # Supports two modes:
    # 1. Simple: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables
    # 2. Advanced: Vaultwarden integration (requires load_telegram_config from alerts.sh)
    load_telegram_config || {
        log_error "Failed to load Telegram config - alert will not be sent"
        return 1
    }

    # Send Telegram alert (simple alert, no state change detection needed)
    log_info "Sending Telegram alert..."
    if send_telegram_alert "aide-failure" "$alert_msg" "🚨"; then
        log_info "✅ Telegram alert sent successfully"
    else
        log_error "❌ Failed to send Telegram alert"
        return 1
    fi

    log_info "=========================================="
    log_info "AIDE Failure Alert completed"
    log_info "=========================================="
}

# Run main function
main "$@"
