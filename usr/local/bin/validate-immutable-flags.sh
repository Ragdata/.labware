#!/bin/bash
# validate-immutable-flags.sh - AIDE Immutable Flag Validation
# Validates immutable flags on AIDE components
#
# Usage: ./validate-immutable-flags.sh
# Exit Codes: 0=All protected, 1=Some missing

set -euo pipefail

# Files to check
AIDE_BINARY="/usr/bin/aide"
AIDE_CONFIG="/etc/aide/aide.conf"
AIDE_DB="/var/lib/aide/aide.db"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Banner
echo "========================================"
echo "AIDE Immutable Flag Validation"
echo "========================================"
echo ""

# Exit code tracker
EXIT_CODE=0

check_immutable() {
    local file="$1"
    local required="${2:-true}"
    local description="$3"

    echo -n "Checking ${description}... "

    # Check if file exists
    if [[ ! -f "$file" ]]; then
        echo -e "${YELLOW}⚠️  File does not exist${NC}"
        if [[ "$required" == "true" ]]; then
            return 1
        else
            return 0
        fi
    fi

    # Check immutable flag
    if lsattr "$file" 2>/dev/null | grep -qE '^[^[:space:]]*i'; then
        echo -e "${GREEN}✅ Protected${NC}"
        return 0
    else
        if [[ "$required" == "true" ]]; then
            echo -e "${RED}❌ NOT Protected (REQUIRED)${NC}"
            echo "  Fix: sudo chattr +i $file"
            return 1
        else
            echo -e "${YELLOW}⚠️  NOT Protected (optional)${NC}"
            return 0
        fi
    fi
}

# Validation
check_immutable "$AIDE_BINARY" true "AIDE binary" || EXIT_CODE=1
check_immutable "$AIDE_CONFIG" true "AIDE config" || EXIT_CODE=1
check_immutable "$AIDE_DB" false "AIDE database" || true

# Show current flags
echo ""
echo "Current immutable flags:"
echo "----------------------------------------"
if [[ -f "$AIDE_BINARY" ]]; then
    echo -n "Binary:   "
    lsattr "$AIDE_BINARY" 2>/dev/null || echo "Cannot read attributes"
fi
if [[ -f "$AIDE_CONFIG" ]]; then
    echo -n "Config:   "
    lsattr "$AIDE_CONFIG" 2>/dev/null || echo "Cannot read attributes"
fi
if [[ -f "$AIDE_DB" ]]; then
    echo -n "Database: "
    lsattr "$AIDE_DB" 2>/dev/null || echo "Cannot read attributes"
fi
echo "----------------------------------------"

# Summary
echo ""
echo "Legend:"
echo "  'i' = immutable flag (file protected)"
echo "  'e' = extent format (default for ext4)"
echo ""

if [[ $EXIT_CODE -eq 0 ]]; then
    echo -e "${GREEN}✅ Validation PASSED - All required files are protected${NC}"
else
    echo -e "${RED}❌ Validation FAILED - Some required files are NOT protected${NC}"
    echo ""
    echo "To protect files:"
    echo "  sudo chattr +i /usr/bin/aide"
    echo "  sudo chattr +i /etc/aide/aide.conf"
    echo ""
    echo "To remove protection (e.g., before APT upgrade):"
    echo "  sudo chattr -i /usr/bin/aide"
fi

exit $EXIT_CODE
