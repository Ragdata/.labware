#!/bin/bash
# /usr/local/bin/rkhunter-daily-scan.sh
# Comprehensive daily rkhunter security scan script

#############################################
# Configuration Variables
#############################################

# Email settings
ADMIN_EMAIL="admin@example.com"
HOSTNAME=$(hostname -f)

# Log files
SCAN_LOG="/var/log/rkhunter-daily.log"
SUMMARY_LOG="/var/log/rkhunter-summary.log"

# Timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

#############################################
# Functions
#############################################

log_message() {
    echo "[$TIMESTAMP] $1" >> "$SCAN_LOG"
}

send_alert() {
    local subject="$1"
    local body="$2"
    echo "$body" | mail -s "$subject" "$ADMIN_EMAIL"
}

#############################################
# Main Script
#############################################

# Start logging
log_message "Starting rkhunter daily scan"

# Update the database first
log_message "Updating rkhunter database"
/usr/bin/rkhunter --update >> "$SCAN_LOG" 2>&1

# Run the scan
log_message "Running security scan"
/usr/bin/rkhunter --check \
    --skip-keypress \
    --report-warnings-only \
    --appendlog \
    --nocolors >> "$SCAN_LOG" 2>&1

SCAN_EXIT_CODE=$?

# Check for warnings
WARNING_COUNT=$(grep -c "\[ Warning \]" /var/log/rkhunter.log 2>/dev/null || echo "0")

# Generate summary
{
    echo "=== rkhunter Daily Scan Summary ==="
    echo "Host: $HOSTNAME"
    echo "Date: $TIMESTAMP"
    echo "Exit Code: $SCAN_EXIT_CODE"
    echo "Warnings Found: $WARNING_COUNT"
    echo ""

    if [ "$WARNING_COUNT" -gt 0 ]; then
        echo "=== Warnings ==="
        grep "\[ Warning \]" /var/log/rkhunter.log
    fi
} > "$SUMMARY_LOG"

# Send email if warnings found
if [ "$WARNING_COUNT" -gt 0 ]; then
    log_message "Warnings detected - sending alert email"
    send_alert "[SECURITY ALERT] rkhunter warnings on $HOSTNAME" "$(cat $SUMMARY_LOG)"
fi

# Log completion
log_message "Daily scan completed. Warnings: $WARNING_COUNT"

exit $SCAN_EXIT_CODE
