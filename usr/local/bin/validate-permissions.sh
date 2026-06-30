#!/bin/bash
# validate-permissions.sh - AIDE Permission Validation
# Validates AIDE directory and file permissions for monitoring access
#
# Usage: ./validate-permissions.sh [monitoring-user]
# Exit Codes: 0=OK, 1=Error

set -euo pipefail

# Configuration
AIDE_DIR="/var/lib/aide"
AIDE_DB="${AIDE_DIR}/aide.db"
AIDE_GROUP="${AIDE_GROUP:-_aide}"
MONITORING_USER="${1:-monitoring-user}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Banner
echo "========================================"
echo "AIDE Permission Validation"
echo "========================================"
echo "Monitoring User: ${MONITORING_USER}"
echo "AIDE Group: ${AIDE_GROUP}"
echo ""

# Exit code tracker
EXIT_CODE=0

# Check 1: _aide group exists
echo -n "Checking if group '${AIDE_GROUP}' exists... "
if getent group "${AIDE_GROUP}" >/dev/null 2>&1; then
    echo -e "${GREEN}✅ OK${NC}"
else
    echo -e "${RED}❌ FAILED${NC}"
    echo "  Fix: sudo groupadd --system ${AIDE_GROUP}"
    EXIT_CODE=1
fi

# Check 2: User exists
echo -n "Checking if user '${MONITORING_USER}' exists... "
if id "${MONITORING_USER}" >/dev/null 2>&1; then
    echo -e "${GREEN}✅ OK${NC}"
else
    echo -e "${RED}❌ FAILED${NC}"
    echo "  Error: User '${MONITORING_USER}' does not exist"
    EXIT_CODE=1
fi

# Check 3: User is in _aide group
echo -n "Checking if user is in '${AIDE_GROUP}' group... "
if groups "${MONITORING_USER}" 2>/dev/null | grep -q "${AIDE_GROUP}"; then
    echo -e "${GREEN}✅ OK${NC}"
else
    echo -e "${RED}❌ FAILED${NC}"
    echo "  Fix: sudo usermod -aG ${AIDE_GROUP} ${MONITORING_USER}"
    EXIT_CODE=1
fi

# Check 4: AIDE directory exists
echo -n "Checking if AIDE directory exists... "
if [[ -d "${AIDE_DIR}" ]]; then
    echo -e "${GREEN}✅ OK${NC}"
else
    echo -e "${RED}❌ FAILED${NC}"
    echo "  Error: Directory '${AIDE_DIR}' does not exist"
    EXIT_CODE=1
fi

# Check 5: Directory permissions (750)
echo -n "Checking directory permissions... "
if [[ -d "${AIDE_DIR}" ]]; then
    DIR_PERMS=$(stat -c '%a' "${AIDE_DIR}")
    DIR_OWNER=$(stat -c '%U:%G' "${AIDE_DIR}")

    if [[ "${DIR_PERMS}" == "750" ]] && [[ "${DIR_OWNER}" == "root:${AIDE_GROUP}" ]]; then
        echo -e "${GREEN}✅ OK (${DIR_PERMS} ${DIR_OWNER})${NC}"
    else
        echo -e "${RED}❌ FAILED (${DIR_PERMS} ${DIR_OWNER})${NC}"
        echo "  Expected: 750 root:${AIDE_GROUP}"
        echo "  Fix: sudo chown root:${AIDE_GROUP} ${AIDE_DIR}"
        echo "       sudo chmod 750 ${AIDE_DIR}"
        EXIT_CODE=1
    fi
fi

# Check 6: Database file permissions (640)
echo -n "Checking database file permissions... "
if [[ -f "${AIDE_DB}" ]]; then
    DB_PERMS=$(stat -c '%a' "${AIDE_DB}")
    DB_OWNER=$(stat -c '%U:%G' "${AIDE_DB}")

    if [[ "${DB_PERMS}" == "640" ]] && [[ "${DB_OWNER}" == "root:${AIDE_GROUP}" ]]; then
        echo -e "${GREEN}✅ OK (${DB_PERMS} ${DB_OWNER})${NC}"
    else
        echo -e "${RED}❌ FAILED (${DB_PERMS} ${DB_OWNER})${NC}"
        echo "  Expected: 640 root:${AIDE_GROUP}"
        echo "  Fix: sudo chown root:${AIDE_GROUP} ${AIDE_DB}"
        echo "       sudo chmod 640 ${AIDE_DB}"
        EXIT_CODE=1
    fi
else
    echo -e "${YELLOW}⚠️  Database does not exist${NC}"
fi

# Check 7: Read access test
echo -n "Testing read access for user... "
if [[ -f "${AIDE_DB}" ]]; then
    if sudo -u "${MONITORING_USER}" test -r "${AIDE_DB}" 2>/dev/null; then
        echo -e "${GREEN}✅ OK${NC}"
    else
        echo -e "${RED}❌ FAILED${NC}"
        echo "  User cannot read database file"
        EXIT_CODE=1
    fi
else
    echo -e "${YELLOW}⚠️  Skipped (database does not exist)${NC}"
fi

# Summary
echo ""
echo "========================================"
if [[ $EXIT_CODE -eq 0 ]]; then
    echo -e "${GREEN}All validation checks PASSED${NC}"
else
    echo -e "${RED}Validation FAILED${NC}"
fi
echo "========================================"

exit $EXIT_CODE
