#!/bin/bash
# Pre-deployment verification script for pipecatapp Nomad job

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

JOB_FILE="ansible/jobs/pipecatapp.nomad"
if [ -f "/opt/nomad/jobs/pipecatapp.nomad" ]; then
    JOB_FILE="/opt/nomad/jobs/pipecatapp.nomad"
fi

if [ -f "/etc/nomad.d/tls/ca.pem" ]; then
    export NOMAD_ADDR="${NOMAD_ADDR:-https://100.64.0.1:4646}"
    export NOMAD_CACERT="${NOMAD_CACERT:-/etc/nomad.d/tls/ca.pem}"
    export NOMAD_CLIENT_CERT="${NOMAD_CLIENT_CERT:-/etc/nomad.d/tls/cli.cert.pem}"
    export NOMAD_CLIENT_KEY="${NOMAD_CLIENT_KEY:-/etc/nomad.d/tls/cli.key.pem}"
fi

JOB_NAME="pipecat-app"
API_URL="http://localhost:8007/api/status"

echo -e "${BOLD}${YELLOW}🚀 Initiating pre-deployment verification for ${JOB_NAME}...${NC}"

# 1. Deploy the job
if [ ! -f "$JOB_FILE" ]; then
    echo -e "${RED}❌ Job file $JOB_FILE not found!${NC}"
    exit 1
fi

echo "Deploying $JOB_FILE..."
nomad job run -detach "$JOB_FILE"

# 2. Wait for stable running state
echo "Waiting for job to reach running state..."
RETRIES=30
DELAY=5
STABLE=false

for ((i=1; i<=RETRIES; i++)); do
    # Looking for a positive number of running allocs in the summary
    STATUS=$(nomad job status "$JOB_NAME" 2>/dev/null | grep "Summary" -A 2 | tail -n 1)
    if echo "$STATUS" | awk '{if ($4 > 0) print "yes"; else print "no"}' | grep -q "yes"; then
        echo -e "${GREEN}✅ Job has running allocations.${NC}"
        STABLE=true
        break
    fi
    echo "Wait $i/$RETRIES: Job not fully running yet. Retrying in ${DELAY}s..."
    sleep $DELAY
done

if [ "$STABLE" = false ]; then
    echo -e "${RED}❌ Job failed to reach a stable running state.${NC}"
    nomad job status "$JOB_NAME"
    exit 1
fi

# 3. Check for OOM kills and extract an alloc ID
echo "Checking for OOM kills..."
ALLOC_ID=$(nomad job allocs "$JOB_NAME" 2>/dev/null | grep -i "running\|pending\|starting" | awk '{print $1}' | head -n 1)

# Fallback if no specific state alloc is found, just grab the latest
if [ -z "$ALLOC_ID" ]; then
    ALLOC_ID=$(nomad job allocs "$JOB_NAME" 2>/dev/null | awk 'NR>1 {print $1}' | head -n 1)
fi

if [ -z "$ALLOC_ID" ]; then
    echo -e "${RED}❌ No allocation found for $JOB_NAME.${NC}"
    exit 1
fi

ALLOC_STATUS=$(nomad alloc status "$ALLOC_ID" 2>/dev/null || true)
if echo "$ALLOC_STATUS" | grep -iq "OOM"; then
    echo -e "${RED}❌ OOM Kill detected in allocation $ALLOC_ID!${NC}"
    echo "$ALLOC_STATUS" | grep -i "OOM"
    exit 1
fi
echo -e "${GREEN}✅ No OOM kills detected.${NC}"

# 4. Verify /api/status returns 200 OK
echo "Verifying /api/status..."
HTTP_RETRIES=15
HTTP_DELAY=5
API_READY=false

for ((i=1; i<=HTTP_RETRIES; i++)); do
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL" || echo "000")
    if [ "$HTTP_CODE" -eq 200 ]; then
        echo -e "${GREEN}✅ /api/status returned 200 OK!${NC}"
        API_READY=true
        break
    fi
    echo "Wait $i/$HTTP_RETRIES: /api/status returned $HTTP_CODE. Retrying in ${HTTP_DELAY}s..."
    sleep $HTTP_DELAY
done

if [ "$API_READY" = false ]; then
    echo -e "${RED}❌ /api/status failed to return 200 OK.${NC}"
    exit 1
fi

echo -e "\n${BOLD}${GREEN}🎉 Pre-deployment verification successful!${NC}"
exit 0
