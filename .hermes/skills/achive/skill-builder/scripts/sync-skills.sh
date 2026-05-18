#!/bin/bash
#
# sync-skills.sh — Đồng bộ skills từ skills/rebuild/ sang .hermes và .claude
#
# Usage:
#   ./scripts/sync-skills.sh skill1 skill2 skill3     # Sync specific skills
#   ./scripts/sync-skills.sh --all                      # Sync all skills
#   ./scripts/sync-skills.sh --list                     # List available skills
#   ./scripts/sync-skills.sh --dry-run skill1 skill2    # Preview without copying
#   ./scripts/sync-skills.sh --remove-orphans           # Remove skills not in rebuild/
#
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(dirname "$SCRIPT_DIR")"
REBUILD_DIR="$WORKSPACE_DIR/skills/rebuild"
HERMES_DIR="$WORKSPACE_DIR/.hermes/skills"
CLAUDE_DIR="$WORKSPACE_DIR/.claude"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

DRY_RUN=false
REMOVE_ORPHANS=false
SYNC_ALL=false
LIST_ONLY=false
TARGET_SKILLS=()

# Parse args
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --all)
            SYNC_ALL=true
            shift
            ;;
        --list)
            LIST_ONLY=true
            shift
            ;;
        --remove-orphans)
            REMOVE_ORPHANS=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [options] [skill1 skill2 ...]"
            echo ""
            echo "Options:"
            echo "  --all              Sync ALL skills in rebuild/"
            echo "  --list             List available skills in rebuild/"
            echo "  --dry-run          Preview changes without copying"
            echo "  --remove-orphans   Remove skills not in rebuild/"
            echo "  --help, -h         Show this help"
            echo ""
            echo "Examples:"
            echo "  $0 prompt-cleaner skill-builder skill-architect"
            echo "  $0 --all"
            echo "  $0 --dry-run prompt-cleaner"
            echo "  $0 --list"
            exit 0
            ;;
        -*)
            echo "Unknown option: $1"
            exit 1
            ;;
        *)
            TARGET_SKILLS+=("$1")
            shift
            ;;
    esac
done

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Check rebuild dir exists
if [[ ! -d "$REBUILD_DIR" ]]; then
    log_error "Rebuild directory not found: $REBUILD_DIR"
    exit 1
fi

# Get available skills (directories with SKILL.md)
get_available_skills() {
    find "$REBUILD_DIR" -maxdepth 2 -name "SKILL.md" -type f 2>/dev/null | \
        sed "s|$REBUILD_DIR/||" | cut -d'/' -f1 | sort -u
}

# List available skills
if [[ "$LIST_ONLY" == true ]]; then
    echo ""
    echo -e "${CYAN}Available skills in rebuild/:${NC}"
    echo ""

    list_skill_status() {
        local skill="$1"
        local src="$REBUILD_DIR/$skill"
        local dest="$HERMES_DIR/$skill"
        local status=""

        if [[ -d "$dest" ]]; then
            local src_time=$(stat -c %Y "$src/SKILL.md" 2>/dev/null || echo "0")
            local dest_time=$(stat -c %Y "$dest/SKILL.md" 2>/dev/null || echo "0")
            if [[ "$src_time" -gt "$dest_time" ]]; then
                status="${YELLOW}[OUTDATED]${NC}"
            else
                status="${GREEN}[UP-TO-DATE]${NC}"
            fi
        else
            status="${CYAN}[NEW]${NC}"
        fi

        printf "  %-30s %s\n" "$skill" "$status"
    }

    while IFS= read -r skill; do
        list_skill_status "$skill"
    done < <(get_available_skills)
    echo ""
    exit 0
fi

# Resolve skills to sync
resolve_skills() {
    local resolved=()

    if [[ "$SYNC_ALL" == true ]]; then
        # All skills
        while IFS= read -r skill; do
            resolved+=("$skill")
        done < <(get_available_skills)
    elif [[ ${#TARGET_SKILLS[@]} -gt 0 ]]; then
        # User-specified skills
        for skill in "${TARGET_SKILLS[@]}"; do
            if [[ -d "$REBUILD_DIR/$skill" ]]; then
                if [[ -f "$REBUILD_DIR/$skill/SKILL.md" ]]; then
                    resolved+=("$skill")
                else
                    log_warn "Skipping '$skill' — no SKILL.md found"
                fi
            else
                log_error "Skill not found: $skill"
                exit 1
            fi
        done
    else
        log_error "No skills specified. Use --all or list skill names."
        echo "Run '$0 --help' for usage."
        exit 1
    fi

    # Print each skill on separate line for mapfile
    printf '%s\n' "${resolved[@]}"
}

# Sync one skill
sync_skill() {
    local skill_name="$1"
    local src="$REBUILD_DIR/$skill_name"
    local dest_hermes="$HERMES_DIR/$skill_name"
    local dest_claude="$CLAUDE_DIR/$skill_name"

    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  Syncing: $skill_name${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

    # Check if skill has SKILL.md
    if [[ ! -f "$src/SKILL.md" ]]; then
        log_warn "No SKILL.md found in $src — skipping"
        return 1
    fi

    # Show files to be synced
    echo "  Files:"
    find "$src" -type f | sed "s|$src|  - |" | head -10
    if [[ $(find "$src" -type f | wc -l) -gt 10 ]]; then
        echo "  ... and more"
    fi

    # Copy to .hermes/skills/
    if [[ -d "$dest_hermes" ]]; then
        if [[ "$DRY_RUN" == true ]]; then
            echo -e "  ${YELLOW}[DRY-RUN]${NC} Would UPDATE: $dest_hermes/"
        else
            log_info "Updating: $dest_hermes/"
            rm -rf "$dest_hermes"
            cp -r "$src" "$dest_hermes"
            log_success "Synced to .hermes/skills/$skill_name/"
        fi
    else
        if [[ "$DRY_RUN" == true ]]; then
            echo -e "  ${YELLOW}[DRY-RUN]${NC} Would CREATE: $dest_hermes/"
        else
            log_info "Creating: $dest_hermes/"
            cp -r "$src" "$dest_hermes"
            log_success "Created .hermes/skills/$skill_name/"
        fi
    fi

    # Copy to .claude/ (if skill has agents/ or skills/ subdirs)
    if [[ -d "$src/agents" ]] || [[ -d "$src/skills" ]]; then
        mkdir -p "$dest_claude"
        if [[ "$DRY_RUN" == true ]]; then
            echo -e "  ${YELLOW}[DRY-RUN]${NC} Would UPDATE: $dest_claude/"
        else
            log_info "Updating: $dest_claude/"
            [[ -d "$src/agents" ]] && cp -r "$src/agents" "$dest_claude/" || true
            [[ -d "$src/skills" ]] && cp -r "$src/skills" "$dest_claude/" || true
            log_success "Synced to .claude/$skill_name/"
        fi
    fi

    return 0
}

# Remove orphans
remove_orphans() {
    echo ""
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${RED}  Checking for orphan skills...${NC}"
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

    local orphans=0
    mapfile -t available < <(get_available_skills)

    for dir in "$HERMES_DIR"/*/; do
        [[ -d "$dir" ]] || continue
        local skill_name="$(basename "$dir")"
        local is_available=false

        for avail in "${available[@]}"; do
            [[ "$avail" == "$skill_name" ]] && is_available=true && break
        done

        if [[ "$is_available" == false ]]; then
            if [[ "$DRY_RUN" == true ]]; then
                echo -e "  ${YELLOW}[DRY-RUN]${NC} Would REMOVE: $dir"
            else
                log_warn "Removing orphan: $skill_name"
                rm -rf "$dir"
                log_success "Removed .hermes/skills/$skill_name/"
            fi
            ((orphans++))
        fi
    done

    if [[ $orphans -eq 0 ]]; then
        log_success "No orphans found"
    else
        log_info "Removed $orphans orphan skill(s)"
    fi
}

# Main
echo ""
log_info "Starting skill sync..."
echo ""
echo "Source:      $REBUILD_DIR"
echo "Target:      $HERMES_DIR"
[[ "$DRY_RUN" == true ]] && echo "Mode:        ${YELLOW}DRY-RUN${NC} (no changes will be made)"
[[ "$REMOVE_ORPHANS" == true ]] && echo "Orphans:     Will be removed"
echo ""

# Resolve skills
mapfile -t SKILLS_TO_SYNC < <(resolve_skills)

if [[ ${#SKILLS_TO_SYNC[@]} -eq 0 ]]; then
    log_warn "No skills to sync"
    exit 0
fi

echo -e "${GREEN}Skills to sync (${#SKILLS_TO_SYNC[@]}):${NC}"
for s in "${SKILLS_TO_SYNC[@]}"; do
    echo "  - $s"
done
echo ""

# Sync each skill
SYNCED=0
SKIPPED=0

for skill in "${SKILLS_TO_SYNC[@]}"; do
    sync_skill "$skill" && ((SYNCED++)) || ((SKIPPED++))
done

# Remove orphans if requested
[[ "$REMOVE_ORPHANS" == true ]] && remove_orphans

# Summary
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  Sync Complete${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo "  Synced:  $SYNCED"
[[ $SKIPPED -gt 0 ]] && echo "  Skipped: $SKIPPED"
echo ""
