#!/bin/bash
#
# 爛 Gag Discord Monitor
# 監察 #gag channel 嘅新訊息，自動解析並提交到 GitHub
#
# Usage: ./gag-discord-monitor.sh
# Cron: */30 * * * * /home/node/.openclaw/workspace/scripts/gag-discord-monitor.sh >> /tmp/gag-monitor.log 2>&1
#

set -e

WORKSPACE="/home/node/.openclaw/workspace"
STATE_FILE="$WORKSPACE/memory/gag-discord-state.json"
GAG_FILE="$WORKSPACE/mini-games/gag/gags.json"
GITHUB_OWNER="raycoderhk"
GITHUB_REPO="mini-games"
GITHUB_PATH="gag/gags.json"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Load state
load_state() {
    if [ -f "$STATE_FILE" ]; then
        cat "$STATE_FILE"
    else
        echo '{"last_check": null, "processed_messages": []}'
    fi
}

# Save state
save_state() {
    echo "$1" > "$STATE_FILE"
}

# Get GitHub token from environment or pass
get_github_token() {
    if [ -n "$GITHUB_TOKEN" ]; then
        echo "$GITHUB_TOKEN"
    else
        log "${RED}❌ GITHUB_TOKEN not set${NC}"
        exit 1
    fi
}

# Get file SHA from GitHub
get_file_sha() {
    local token=$(get_github_token)
    local sha=$(curl -s \
        -H "Authorization: token $token" \
        -H "Accept: application/vnd.github.v3+json" \
        "https://api.github.com/repos/$GITHUB_OWNER/$GITHUB_REPO/contents/$GITHUB_PATH" \
        | jq -r '.sha')
    echo "$sha"
}

# Add gag to gags.json and commit
add_gag() {
    local question="$1"
    local answer="$2"
    local author="$3"
    
    if [ -z "$question" ] || [ -z "$answer" ]; then
        log "${RED}❌ Missing question or answer${NC}"
        return 1
    fi
    
    if [ -z "$author" ]; then
        author="@Unknown"
    fi
    
    local token=$(get_github_token)
    local sha=$(get_file_sha)
    
    if [ -z "$sha" ]; then
        log "${RED}❌ Cannot get file SHA${NC}"
        return 1
    fi
    
    # Get current gags
    local current_gags=$(curl -s "https://raw.githubusercontent.com/$GITHUB_OWNER/$GITHUB_REPO/main/$GITHUB_PATH")
    
    # Create new gag entry
    local new_gag=$(cat <<EOF
{
    "id": $(date +%s)000,
    "question": "$question",
    "answer": "$answer",
    "author": "$author",
    "date": "$(date -Iseconds)"
}
EOF
)
    
    # Add to beginning of array (using jq)
    local updated_gags=$(echo "$current_gags" | jq --argjson new "$new_gag" '. = [$new] + .')
    
    # Convert to base64
    local content=$(echo "$updated_gags" | base64 -w 0)
    
    # Commit to GitHub
    local commit_msg="🥚 Add new gag from Discord by $author: ${question:0:30}..."
    
    local response=$(curl -s -X PUT \
        -H "Authorization: token $token" \
        -H "Accept: application/vnd.github.v3+json" \
        -H "Content-Type: application/json" \
        "https://api.github.com/repos/$GITHUB_OWNER/$GITHUB_REPO/contents/$GITHUB_PATH" \
        -d "{
            \"message\": \"$commit_msg\",
            \"content\": \"$content\",
            \"sha\": \"$sha\"
        }")
    
    if echo "$response" | jq -e '.commit' > /dev/null; then
        log "${GREEN}✅ Committed: $commit_msg${NC}"
        return 0
    else
        log "${RED}❌ Commit failed: $response${NC}"
        return 1
    fi
}

# Parse message content for gag
parse_gag() {
    local content="$1"
    local question=""
    local answer=""
    local author=""
    
    # Try to parse with labels
    if echo "$content" | grep -qi "題目："; then
        question=$(echo "$content" | grep -i "題目：" | head -1 | sed 's/題目：//i' | xargs)
    fi
    
    if echo "$content" | grep -qi "答案："; then
        answer=$(echo "$content" | grep -i "答案：" | head -1 | sed 's/答案：//i' | xargs)
    fi
    
    if echo "$content" | grep -qi "出品人："; then
        author=$(echo "$content" | grep -i "出品人：" | head -1 | sed 's/出品人：//i' | xargs)
    elif echo "$content" | grep -q "@"; then
        author=$(echo "$content" | grep "@" | tail -1 | xargs)
    fi
    
    # If no labels, try line-by-line
    if [ -z "$question" ]; then
        question=$(echo "$content" | head -1 | xargs)
    fi
    
    if [ -z "$answer" ]; then
        answer=$(echo "$content" | sed -n '2p' | xargs)
    fi
    
    echo "$question|$answer|$author"
}

# Main function
main() {
    log "${YELLOW}🔍 Checking Discord #gag channel...${NC}"
    
    # Note: This script requires Discord API access
    # For OpenClaw integration, use the message tool instead
    
    log "${YELLOW}ℹ️  Discord integration requires OpenClaw message API${NC}"
    log "${YELLOW}ℹ️  For now, use Admin Panel or send gags for manual processing${NC}"
    
    # In real implementation:
    # 1. Call OpenClaw message tool to get recent messages
    # 2. Parse each message
    # 3. Add valid gags to GitHub
    # 4. Update state file
    
    exit 0
}

main "$@"
