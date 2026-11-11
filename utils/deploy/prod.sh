#!/usr/bin/env bash
set -euo pipefail

# ============================================================================
# motoproponent — Production deploy to Synology NAS (Docker-on-NAS, standalone)
#
# Static holding page served by nginx in a container, fronted by the existing
# Cloudflare Tunnel. See docs/nas-setup.md for the one-time bringup.
# ============================================================================

# Configuration
NAS_USER="ziad"
NAS_HOST="nas.feralcreative.co"
NAS_SSH_PORT="33725"
NAS_DEPLOY_PATH="/volume1/web/motoproponent.com"
CONTAINER_NAME="motoproponent"
IMAGE_NAME="motoproponent:latest"
HOST_PORT="1480"
TARGET_URL="https://motoproponent.com"

# Colors
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'
CYAN='\033[0;36m'; MAGENTA='\033[0;35m'; BOLD='\033[1m'; DIM='\033[2m'; NC='\033[0m'

log_info()    { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error()   { echo -e "${RED}[ERROR]${NC} $1" >&2; }

format_time() {
  local s=$1
  if [ "$s" -lt 60 ]; then echo "${s}s"; else echo "$((s/60))m $((s%60))s"; fi
}

require_cmd() {
  local cmd=$1 hint=${2:-}
  command -v "$cmd" >/dev/null 2>&1 || { log_error "Required command '$cmd' not found. $hint"; exit 1; }
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_ROOT"

DEPLOY_START=$(date +%s)

# Parse flags
DRY_RUN=""; FORCE=""
for arg in "$@"; do
  case "$arg" in
    --dry-run|-n) DRY_RUN=1 ;;
    --force|-f)   FORCE=1 ;;
    --help|-h)    echo "Usage: $(basename "$0") [--dry-run] [--force]"; exit 0 ;;
    *) log_error "Unknown flag: $arg"; exit 1 ;;
  esac
done

DEPLOY_ENV="prod"

require_cmd docker "Install Docker Desktop."
require_cmd ssh    "OpenSSH client is required."
require_cmd git    "Git is required."

# Load .env
if [ -f "$PROJECT_ROOT/.env" ]; then
  set -a; source "$PROJECT_ROOT/.env"; set +a
fi

# SSH key detection.
# Ziad's keys live in the 1Password SSH agent, so the agent tier is the one that
# normally wins here — expect a Touch ID prompt during the SSH steps below.
check_ssh_key() {
  if [ -n "${SSH_KEY_PATH:-}" ] && [ -f "$SSH_KEY_PATH" ]; then return; fi
  if [ -f "$HOME/.ssh/id_ed25519" ]; then SSH_KEY_PATH="$HOME/.ssh/id_ed25519"; return; fi
  if [ -f "$HOME/.ssh/id_rsa" ];      then SSH_KEY_PATH="$HOME/.ssh/id_rsa";      return; fi
  if ssh-add -l > /dev/null 2>&1;     then USE_SSH_AGENT=1;                       return; fi
  log_error "No SSH key found."; exit 1
}

get_ssh_cmd() {
  local cmd="ssh -p ${NAS_SSH_PORT}"
  [ -z "${USE_SSH_AGENT:-}" ] && [ -n "${SSH_KEY_PATH:-}" ] && cmd="$cmd -i $SSH_KEY_PATH"
  echo "$cmd"
}

check_ssh_key
SSH_CMD="$(get_ssh_cmd)"
NAS="${NAS_USER}@${NAS_HOST}"

# Production safety gates
GIT_SHA=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")

if [ "$DEPLOY_ENV" = "prod" ] && [ -z "${FORCE:-}" ]; then
  if [ -n "$(git status --porcelain)" ]; then
    log_error "Working tree is dirty. Commit/stash, or pass --force."
    exit 1
  fi
  if [ "$GIT_BRANCH" != "main" ]; then
    log_error "Not on 'main' (current: $GIT_BRANCH). Switch or pass --force."
    exit 1
  fi
fi

if [ "$DEPLOY_ENV" = "prod" ] && [ -z "${DRY_RUN:-}" ]; then
  echo ""
  echo -e "${RED}${BOLD}⚠  You are about to deploy to PRODUCTION${NC}"
  echo -e "   URL    : ${BOLD}${TARGET_URL}${NC}"
  echo -e "   Commit : ${BOLD}${GIT_SHA}${NC} on ${BOLD}${GIT_BRANCH}${NC}"
  read -r -p "Type 'yes' to continue: " CONFIRM
  [ "$CONFIRM" = "yes" ] || { log_error "Aborted."; exit 1; }
fi

# ---------------------------------------------------------------- build
log_info "Building ${IMAGE_NAME} (linux/amd64)..."
if [ -n "${DRY_RUN:-}" ]; then
  log_warning "[dry-run] docker build --platform linux/amd64 -t ${IMAGE_NAME} ."
else
  docker build --platform linux/amd64 -t "${IMAGE_NAME}" .
fi

# ---------------------------------------------------------------- transfer
TARBALL="/tmp/${CONTAINER_NAME}-$(date +%s).tar.gz"
log_info "Saving image to ${TARBALL}..."
if [ -n "${DRY_RUN:-}" ]; then
  log_warning "[dry-run] docker save ${IMAGE_NAME} | gzip > ${TARBALL}"
else
  docker save "${IMAGE_NAME}" | gzip > "${TARBALL}"
  log_info "Image size: $(du -h "${TARBALL}" | cut -f1)"
fi

log_info "Ensuring remote directory ${NAS_DEPLOY_PATH}..."
if [ -n "${DRY_RUN:-}" ]; then
  log_warning "[dry-run] ${SSH_CMD} ${NAS} \"mkdir -p ${NAS_DEPLOY_PATH}\""
else
  $SSH_CMD "$NAS" "mkdir -p ${NAS_DEPLOY_PATH}"
fi

log_info "Transferring image to NAS (piped, not scp)..."
if [ -n "${DRY_RUN:-}" ]; then
  log_warning "[dry-run] cat ${TARBALL} | ${SSH_CMD} ${NAS} \"cat > ${NAS_DEPLOY_PATH}/image.tar.gz\""
else
  cat "${TARBALL}" | $SSH_CMD "$NAS" "cat > ${NAS_DEPLOY_PATH}/image.tar.gz"
fi

log_info "Copying docker-compose.yml..."
if [ -n "${DRY_RUN:-}" ]; then
  log_warning "[dry-run] cat docker-compose.yml | ${SSH_CMD} ${NAS} \"cat > ${NAS_DEPLOY_PATH}/docker-compose.yml\""
else
  cat docker-compose.yml | $SSH_CMD "$NAS" "cat > ${NAS_DEPLOY_PATH}/docker-compose.yml"
fi

# ---------------------------------------------------------------- remote up
log_info "Loading image and restarting container on NAS..."
REMOTE_SCRIPT="
set -e
cd ${NAS_DEPLOY_PATH}
/usr/local/bin/docker load < image.tar.gz
/usr/local/bin/docker-compose down || true
/usr/local/bin/docker-compose up -d
rm -f image.tar.gz
"
if [ -n "${DRY_RUN:-}" ]; then
  log_warning "[dry-run] remote: docker load / compose down / compose up -d"
else
  $SSH_CMD "$NAS" "$REMOTE_SCRIPT"
fi

# ---------------------------------------------------------------- verify
if [ -z "${DRY_RUN:-}" ]; then
  log_info "Verifying container is answering on 127.0.0.1:${HOST_PORT}..."
  HTTP_CODE=$($SSH_CMD "$NAS" "curl -s -o /dev/null -w '%{http_code}' --max-time 10 http://127.0.0.1:${HOST_PORT}/ || echo 000")
  if [ "$HTTP_CODE" = "200" ]; then
    log_success "Origin responded 200 on port ${HOST_PORT}."
  else
    log_error "Origin returned '${HTTP_CODE}' on port ${HOST_PORT}. Check: docker logs ${CONTAINER_NAME}"
    exit 1
  fi
fi

# ---------------------------------------------------------------- cleanup
rm -f "${TARBALL}" 2>/dev/null || true

DEPLOY_END=$(date +%s)
echo ""
echo -e "${CYAN}────────────────────────────────────────────────${NC}"
log_success "Deployed ${MAGENTA}${CONTAINER_NAME}${NC} in $(format_time $((DEPLOY_END - DEPLOY_START)))"
echo -e "   ${MAGENTA}Commit${NC} : ${GIT_SHA} on ${GIT_BRANCH}"
echo -e "   ${MAGENTA}Origin${NC} : http://127.0.0.1:${HOST_PORT} (on NAS)"
echo -e "   ${MAGENTA}Public${NC} : ${TARGET_URL}"
echo -e "${CYAN}────────────────────────────────────────────────${NC}"
echo ""
echo -e "${DIM}If the public URL 404s, the tunnel route is missing — see docs/nas-setup.md.${NC}"
